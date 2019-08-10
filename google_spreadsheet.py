import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import settings


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file']


class GoogleSheet:
    def __init__(self, title):
        self.creds = self.autentificate()
        self.new_file_id = self.create_sheet(title)

    def autentificate(self):
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """

        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return creds


    def write_spreadsheet(self, range, values):
        service = build('sheets', 'v4', credentials=self.creds)
        # Call the Sheets API
        sheet = service.spreadsheets()
        body = {
        'range': range,
        'values' : values,
        }
        sheet.values().update(spreadsheetId=self.new_file_id,
                                    range=range,
                                    body=body, valueInputOption="RAW").execute()



    #
    # def get_info():
    #     service = build('sheets', 'v4', credentials=creds)
    #
    #     sheet_metadata = service.spreadsheets().get(spreadsheetId=settings.GOOGLE_SPREADSHEET_ID).execute()
    #     sheets = sheet_metadata.get('sheets', '')
    #     # each sheet in the document contains a set of requirements of the same cathegory
    #     for s in sheets:
    #         # the sheet title, or name, we'll use it to name the outputs related to each sheet
    #         title = s.get("properties", {}) #.get("sheetId", "")
    #         print(title)
    #
    #
    def create_sheet(self, titulo):
        service = build('sheets', 'v4', credentials=self.creds)
        body = {
            "properties": {
              "title": titulo,
            },
        }
        request = service.spreadsheets().create(body=body)
        response = request.execute()
        # print(response)
        spreadsheetId = response['spreadsheetId']
        # print(spreadsheetId)
        drive_service = build('drive', 'v3', credentials=self.creds)

        # Retrieve the existing parents to remove
        file = drive_service.files().get(fileId=spreadsheetId,
                                         fields='parents').execute();
        previous_parents = ",".join(file.get('parents'))
        # Move the file to the new folder
        file = drive_service.files().update(fileId=spreadsheetId,
                                            addParents=settings.GOOGLE_FOLDER,
                                            removeParents=previous_parents,
                                            fields='id, parents').execute()
        return spreadsheetId


    def create_summary(self, projects, engineers):
        title = "summary"
        sheetId = self.get_tab_from_template(settings.TEMPLATE_SUMARY, title)
        start = 12
        end = start + len(projects) - 1
        range = '{}!A{}:B{}'.format(title, start, end)
        values = []
        for project in projects:
            values.append([project, projects[project]])
        print(values)
        print(range)
        self.write_spreadsheet(range, values)
        # engineers
        for engineer in engineers:
            pass



    def get_tab_from_template(self, tab_id, title):
        service = build('sheets', 'v4', credentials=self.creds)
        # Call the Sheets API
        sheet = service.spreadsheets()

        copy_sheet_to_another_spreadsheet_request_body = {
            # The ID of the spreadsheet to copy the sheet to.
            'destination_spreadsheet_id': self.new_file_id,

            # TODO: Add desired entries to the request body.
        }

        request = service.spreadsheets().sheets().copyTo(spreadsheetId=settings.GOOGLE_SPREADSHEET_ID, sheetId=tab_id,
                                                         body=copy_sheet_to_another_spreadsheet_request_body)
        response = request.execute()
        # print(response)
        new_sheetId = response['sheetId']
        # RENAME
        body = {
            "requests": {
                "updateSheetProperties": {
                    "properties": {
                        "sheetId": new_sheetId,
                        "title": title,
                    },
                    "fields": "title",
                },
            }
        }
        service.spreadsheets().batchUpdate(spreadsheetId=self.new_file_id, body=body).execute()
        return new_sheetId


    def delete_sheet(self, sheetId):
        service = build('sheets', 'v4', credentials=self.creds)
        body = {
            "requests": {
                "deleteSheet": {
                    "sheetId": sheetId,
                },
            }
        }
        service.spreadsheets().batchUpdate(spreadsheetId=self.new_file_id, body=body).execute()

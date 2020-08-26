import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
import io
import settings
import os

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file']


class GoogleSheet:
    def __init__(self, title):
        self._authenticate()
        # Call the Sheets API
        service = build('sheets', 'v4', credentials=self.creds)
        self.sheet = service.spreadsheets()
        self._create_spreadsheet(title)
        self.title = title

    def _authenticate(self):
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        creds = None
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
        self.creds = creds

    def _write_values(self, range, values):
        body = {
            'range': range,
            'values': values,
        }
        self.sheet.values().update(spreadsheetId=self.spreadsheet_id, range=range,
                                   body=body, valueInputOption="RAW").execute()

    def _append_values(self, range, values):
        body = {
            'range': range,
            'values': values,
        }
        self.sheet.values().append(spreadsheetId=self.spreadsheet_id, range=range,
                                   body=body, valueInputOption="RAW", insertDataOption="INSERT_ROWS").execute()

    # def get_info():
    #     sheet_metadata = self.sheet.get(spreadsheetId=settings.GOOGLE_TEMPLATE_SPREADSHEET).execute()
    #     sheets = sheet_metadata.get('sheets', '')
    #     # each sheet in the document contains a set of requirements of the same cathegory
    #     for s in sheets:
    #         # the sheet title, or name, we'll use it to name the outputs related to each sheet
    #         title = s.get("properties", {}) #.get("sheetId", "")
    #         print(title)

    def _create_spreadsheet(self, titulo):
        body = {
            "properties": {
                "title": titulo,
            },
        }
        response = self.sheet.create(body=body).execute()
        # print(response)
        self.spreadsheet_id = response['spreadsheetId']
        if settings.GOOGLE_FOLDER is not None:  # move to the destination folder
            drive_service = build('drive', 'v3', credentials=self.creds)
            # Retrieve the existing parents to remove
            file = drive_service.files().get(fileId=self.spreadsheet_id, fields='parents').execute()
            previous_parents = ",".join(file.get('parents'))
            # Add the new folder and remove the old ones
            drive_service.files().update(fileId=self.spreadsheet_id, addParents=settings.GOOGLE_FOLDER,
                                         removeParents=previous_parents, fields='id, parents').execute()

    def create_summary(self, projects, engineers_and_vals):
        title = "Summary"
        start_row = 6
        sheetId = self.get_tab_from_template(settings.TEMPLATE_SUMARY, title)
        # fill projects
        end_row = start_row + 1 + len(projects) - 1
        range = '{}!A{}:A{}'.format(title, start_row + 1, end_row)
        values = []
        for project in projects:
            values.append([project, ])
        self._write_values(range, values)
        # fill engineers and their hours
        n_engineers = len(engineers_and_vals[0])
        startLetter = "C"
        endLetter = chr(ord(startLetter) + n_engineers - 1)
        # engineers_and_vals.insert(1, [None, None, None])  # empty row to match the template (not needed any more)
        range = '{}!{}{}:{}{}'.format(title, startLetter, start_row, endLetter, end_row)
        self._write_values(range, engineers_and_vals)
        # hide empty rows and columns
        requests = []
        requests.append({"setBasicFilter": {
            "filter": {
                "range": {
                    "sheetId": sheetId,
                    "startRowIndex": 5,
                    "endRowIndex": 18,
                    "startColumnIndex": 0,
                    "endColumnIndex": 12
                },
                "criteria": {
                    "0": {
                        "condition": {
                            "type": "NOT_BLANK",
                        }
                    }
                }
            }
        }})
        requests.append({'updateDimensionProperties': {
            "range": {
                "sheetId": sheetId,
                "dimension": 'COLUMNS',
                "startIndex": n_engineers + 2,
                "endIndex": 12,
            },
            "properties": {
                "hiddenByUser": True,
            },
            "fields": 'hiddenByUser',
        }})
        body = {'requests': requests}
        self.sheet.batchUpdate(spreadsheetId=self.spreadsheet_id, body=body).execute()

    def create_project(self, project, prj_idx, registers):
        sheetId = self.get_tab_from_template(settings.TEMPLATE_PROJECT, project)
        range = '{}!{}'.format(project, settings.PRJ_ROW)
        values = [[7 + prj_idx, ], ]
        self._write_values(range, values)
        self.hide_0_hours_entries(sheetId, 9, 20, 0, 4)

        startLetter = "A"
        endLetter = "C"
        range = '{}!{}{}:{}{}'.format(project, startLetter, 30, endLetter, 30 + len(registers))
        print(range)
        self._write_values(range, registers)


    def create_engineer(self, engineer, eng_idx):
        sheetId = self.get_tab_from_template(settings.TEMPLATE_ENGINEER, engineer)
        range = '{}!{}'.format(engineer, settings.ENG_ROW)
        values = [[3 + eng_idx, ], ]
        self._write_values(range, values)
        self.hide_0_hours_entries(sheetId, 9, 22, 0, 4)

    def create_detailed_project(self, project, period):
        sheetId = self.get_tab_from_template(settings.TEMPLATE_DETAILED_PROJECT , project)
        range = '{}!{}'.format(project, settings.PRJ_CELL)
        self._write_values(range, [[project,],])
        range = '{}!{}'.format(project, settings.DATE_CELL)
        self._write_values(range, [[period,],])

    def append_project_summary(self, project, prj_regs):
        startLetter = "A"
        endLetter = "B"
        summary_row = 9
        range = '{}!{}{}:{}'.format(project, startLetter, summary_row, endLetter)
        range = 'A9'
        print(range)
        self._append_values(range, prj_regs)

    def append_engineer_details(self, project, engineer, worked_days):
        row = 15
        startLetter = "A"
        endLetter = "D"
        range = '{}!{}{}:{}'.format(project, startLetter, row, endLetter)
        print(range)
        self._append_values(range, worked_days)

    def generatePDF(self):
        drive_service = build('drive', 'v3', credentials=self.creds)
        request = drive_service.files().export_media(fileId=self.spreadsheet_id,
                                                     mimeType='application/pdf')
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))

        file_metadata = {'name': self.title + '.pdf', 'parents' : [settings.GOOGLE_FOLDER,] }
        media = MediaIoBaseUpload(fh, mimetype='application/pdf')
        file = drive_service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
        print('File ID: %s' % file.get('id'))


    def get_tab_from_template(self, tab_id, title):
        body = {
            'destination_spreadsheet_id': self.spreadsheet_id,  # The ID of the spreadsheet to copy the sheet to.
        }
        response = self.sheet.sheets().copyTo(spreadsheetId=settings.GOOGLE_TEMPLATE_SPREADSHEET,
                                              sheetId=tab_id, body=body).execute()
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
        self.sheet.batchUpdate(spreadsheetId=self.spreadsheet_id, body=body).execute()
        return new_sheetId

    def delete_sheet(self, sheet_id):
        body = {
            "requests": {
                "deleteSheet": {
                    "sheetId": sheet_id,
                },
            }
        }
        self.sheet.batchUpdate(spreadsheetId=self.spreadsheet_id, body=body).execute()

    def hide_0_hours_entries(self, sheetId, startRowIndex, endRowIndex, startColumnIndex, endColumnIndex):
        body = {
            "requests": {
                "setBasicFilter": {
                    "filter": {
                        "range": {
                            "sheetId": sheetId,
                            "startRowIndex": startRowIndex,
                            "endRowIndex": endRowIndex,
                            "startColumnIndex": startColumnIndex,
                            "endColumnIndex": endColumnIndex,
                        },
                        "sortSpecs": [
                            {
                                "dimensionIndex": 2,
                                "sortOrder": "DESCENDING"
                            }
                        ],
                        "criteria": {
                            "2": {
                                "condition": {
                                    "type": "NUMBER_GREATER",
                                    "values": [{"userEnteredValue": "0"}, ]
                                }
                            }
                        }
                    }
                }
            }
        }
        self.sheet.batchUpdate(spreadsheetId=self.spreadsheet_id, body=body).execute()

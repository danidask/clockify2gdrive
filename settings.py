# DO NOT EDIT THIS FILE, create a local_settings.py

CLOCKIFY_API_KEY = "xxx"
CLOCKIFY_WORKSPACE_ID = "xxx"


GOOGLE_FOLDER = "xxx"  # folder id to move the generated report. None to leave it in the root folder
GOOGLE_TEMPLATE_SPREADSHEET = "xxx"
TEMPLATE_SUMARY = "0"  # SheetId of the sumary sheet inside the template
TEMPLATE_PROJECT = "0"  # SheetId of the project_template sheet inside the template
TEMPLATE_ENGINEER = "0"  # SheetId of the engineer_template sheet inside the template
TEMPLATE_DETAILED_PROJECT = "0" # SheetId of the detailed template
PRJ_CELL = "A1"
DATE_CELL = "A1"
PRJ_ROW = "A1"
ENG_ROW = "A1"

prorated_users = ['Jhon Doe',]
prorated_projects = ['Support project',]

TELEGRAM_TOKEN = "xxx"
telegram_users = {  # name must match clockyfy name
    "Jhon Doe": 1111111,
}

RUNNING_CLOCK_ALERT = 2  # number or hours to trigger the alert

try:
    from local_settings import *
except ImportError:
    print("You must create a local_settings.py file that overrides settings.py variables")
    quit(1)

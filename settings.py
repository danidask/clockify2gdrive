API_KEY = "xxx"
WORKSPACE_ID = "xxx"

GOOGLE_CLIENT_ID = "xxx"
GOOGLE_CLIENT_SECRET = "xxx"

GOOGLE_SPREADSHEET_ID = "xxx"

GOOGLE_FOLDER = "x"

TEMPLATE_SUMARY = "0"
TEMPLATE_PER_PROJECT = "0"
TEMPLATE_PER_ENGINEER = "0"

try:
    from local_settings import *
except ImportError:
    print("You must create a local_settings.py file that overrides settings.py variables")
    quit(1)

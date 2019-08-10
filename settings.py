CLOCKIFY_API_KEY = "xxx"
CLOCKIFY_CLOCKIFY_WORKSPACE_ID = "xxx"

GOOGLE_TEMPLATE_SPREADSHEET = "xxx"
GOOGLE_FOLDER = "xxx"
TEMPLATE_SUMARY = "0"

try:
    from local_settings import *
except ImportError:
    print("You must create a local_settings.py file that overrides settings.py variables")
    quit(1)

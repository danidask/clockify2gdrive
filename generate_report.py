import settings
import clockify
from google_spreadsheet import GoogleSheet

# clockify.get_workspaces()
projects, engineers = clockify.get_reports_summary(7, 2019)
print(projects)
print(engineers)
quit(0)
# {'#3 Modbus IO': 16, '#1 Acrolon target and dev kit': 12, '#5 FTclick': 49}
gsh = GoogleSheet("titulo 777")

gsh.create_summary(projects, engineers)
gsh.delete_sheet(0)  # delete default first sheet

# for engineer in engineers:
#     pass



#
# for project in projects.keys():
#     description = project
#     hours = projects[project]
#     gsh.create_summary(description, hours)



# horas = "PT15H"
# print(hours_from_duration(horas))

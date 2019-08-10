import settings
import clockify
from google_spreadsheet import GoogleSheet

# clockify.get_workspaces()
engineers, projects = clockify.get_reports_summary()
print(engineers)
print(projects)
# {'Miguel Torres': 37, 'Engineer1': 20, 'Engineer2': 20}
# {'#3 Modbus IO': 16, '#1 Acrolon target and dev kit': 12, '#5 FTclick': 49}
gsh = GoogleSheet("titulo 444")

gsh.create_summary(projects)
#
# for project in projects.keys():
#     description = project
#     hours = projects[project]
#     gsh.create_summary(description, hours)



# horas = "PT15H"
# print(hours_from_duration(horas))

import clockify
from google_spreadsheet import GoogleSheet
import pandas as pd
from miscellanea import get_past_month


# clockify.get_workspaces()
month, year = get_past_month()
projects, engineers, registers = clockify.get_reports_summary(month, year)
# print(projects)  # {'#5 FTclick', '#3 Modbus IO', '#1  target and dev kit'}
# print(engineers)  # {'Engineer2', 'Jhon Doe', 'Engineer1'}
# print(registers)  # [('#3 Modbus IO', 'Jhon Doe', 1), ('#1  target and dev kit', 'Jhon Doe', 2), ('#5 FTclick', 'Jhon Doe', 4), ('#5 FTclick', 'Jhon Doe', 15), ('#5 FTclick', 'Jhon Doe', 15), ('#3 Modbus IO', 'Engineer1', 5), ('#5 FTclick', 'Engineer1', 15), ('#3 Modbus IO', 'Engineer2', 10), ('#1  target and dev kit', 'Engineer2', 10)]

# prepare the values using a pandas table
df = pd.DataFrame(0, index=projects, columns=engineers)
for register in registers:
    df.at[register[0], register[1]] += register[2]
a = df.columns.values.tolist()
vals = df.values.tolist()
vals.insert(0, a)
# print (vals)  # [['Engineer2', 'Engineer1', 'Jhon Doe'], [0, 15, 34], [10, 0, 2], [10, 5, 1]]

title = "timesheet {}-{}".format(year, month)
gsh = GoogleSheet(title)
gsh.create_summary(projects, vals)
gsh.delete_sheet(0)  # delete default first sheet

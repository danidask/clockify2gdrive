import clockify
from google_spreadsheet import GoogleSheet
import pandas as pd
from miscellanea import get_past_month_start_end, get_past_month_str
import settings

# clockify.get_workspaces()
print("-> Getting clockify reports...")
start, end = get_past_month_start_end()
period = get_past_month_str()
print(start, end, period)
projects, engineers, registers = clockify.get_reports_summary(start, end)
#print(projects)  # ['#5 FTclick', '#3 Modbus IO', '#1  target and dev kit']
#print(engineers)  # ['Engineer2', 'Jhon Doe', 'Engineer1']
#print(registers)  # [('#3 Modbus IO', 'Jhon Doe', 1), ('#1  target and dev kit', 'Jhon Doe', 2), ('#5 FTclick', 'Jhon Doe', 4), ('#5 FTclick', 'Jhon Doe', 15), ('#5 FTclick', 'Jhon Doe', 15), ('#3 Modbus IO', 'Engineer1', 5), ('#5 FTclick', 'Engineer1', 15), ('#3 Modbus IO', 'Engineer2', 10), ('#1  target and dev kit', 'Engineer2', 10)]

print("-> Creating spreadsheet...")
# prepare the values using a pandas table
projects.sort()
engineers.sort()
df = pd.DataFrame(0, index=projects, columns=engineers, dtype='float')
for register in registers:
    df.at[register[0], register[1]] += register[2]
a = df.columns.values.tolist()
vals = df.values.tolist()
vals.insert(0, a)
#print (vals)  # [['Engineer2', 'Engineer1', 'Jhon Doe'], [0, 15, 34], [10, 0, 2], [10, 5, 1]]

df_all = pd.DataFrame(registers, columns=('project', 'username', 'duration', 'description', 'date', 'end'))
print(projects)
project_entries = df_all.groupby(['project', 'username'])['duration'].sum()
print(project_entries)

# --------------- WIP -------------------------------------
# prorate projects
billable_projects = list(set(projects) - set(settings.prorated_projects))
print(billable_projects)
# calculate billable projects ratios
billable_prj_entries = df_all[df_all['project'].isin(billable_projects)].groupby(['project'])['duration'].sum()
billable_prj_sum = billable_prj_entries.sum()
print('billable sum:', billable_prj_sum, billable_prj_entries)
billable_prj_ratios = billable_prj_entries / billable_prj_sum
print(billable_prj_ratios, billable_prj_ratios.sum())
# spread prorated projects
for project in projects:
    if project in settings.prorated_projects:
        print(project, ' entries:\n', project_entries[project], '\ntotal: ', project_entries[project].sum())
        print(project_entries.groupby(['project']).sum(), project_entries.groupby(['project']).sum().sum())
        project_sum = project_entries[project].sum()
        prorated_hours = billable_prj_ratios * project_sum
        print(prorated_hours)
# --------------- END WIP -------------------------------------

#print(df_all)
#df_all.to_pickle("hours.pkl")
# --------------- generate detailed projects timesheets ----------
for project in projects:
    print('----------------------',project,'----------------------')
    print(project_entries[project])
    names = project_entries[project].index.tolist()
    hours = project_entries[project].values.tolist()
    prj_regs = list(zip(names, hours))
    title = "timesheet {} {}".format(period, project)
    gsh = GoogleSheet(title)
    # summary per engineer and total
    print(prj_regs)
    gsh.create_detailed_project(project, period)
    gsh.delete_sheet(0)  # delete default first sheet
    # details per engineer and day
    for engineer in engineers:
        if (df.loc[project, engineer] > 0):
            print(engineer)
            if (engineer not in settings.prorated_users):
                user_entries = df_all[(df_all['project']==project) & (df_all['username']==engineer)]
                #print(user_entries)
                day_entries = user_entries.groupby(pd.Grouper(key='date', freq='1D'))['username', 'description', 'duration'].agg({'duration' : sum, 'username' : 'last', 'description' : lambda tags: '\n'.join(set(tags))})
                #print(day_entries)
                worked_days = day_entries[day_entries['duration'] > 0.0]
                worked_days['day'] = worked_days.index.strftime('%Y-%m-%d')
                worked_days = worked_days.reindex(columns=['username', 'day', 'description', 'duration'])
                #print(worked_days)
                header = worked_days.columns.tolist()
                eng_regs = worked_days.values.tolist()
                print(eng_regs)
                gsh.append_engineer_details(project, engineer, eng_regs)
            time.sleep(1)
    gsh.append_project_summary(project, prj_regs)
    gsh.generatePDF()

print("Done!")

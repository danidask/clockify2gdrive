import datetime
import json
import requests
import settings
import isodatetime.parsers as parse  # https://pypi.org/project/isodatetime/


base_url = "https://api.clockify.me/api"

headers = {
    "content-type": "application/json",
    "X-Api-Key": settings.CLOCKIFY_API_KEY,
}


def get_start_end_dates(month, year):
    startDate = datetime.datetime.strptime('{}/1/{}'.format(month, year), "%m/%d/%Y")
    month += 1
    if month > 12:
        month = 1
        year += 1
    endDate = datetime.datetime.strptime('{}/1/{}'.format(month, year), "%m/%d/%Y")
    endDate -= datetime.timedelta(milliseconds=1)
    startDateStr = startDate.isoformat()+"Z"
    endDateStr = endDate.isoformat()+"Z"
    # 2019-07-01T00:00:00.000Z
    # print(begin.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
    # print(end.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
    return startDateStr, endDateStr


def get_workspaces():
    url = base_url + "/workspaces/"
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    # print(response.text)
    rj = response.json()
    print("numero de workspaces : {}".format(len(rj)))
    for entrada in rj:
        print(entrada)


def get_reports_summary(month, year):
    url = base_url + "/workspaces/{}/reports/summary/".format(settings.CLOCKIFY_WORKSPACE_ID)
    startDate, endDate = get_start_end_dates(month, year)
    data = {
        # "startDate":"2019-07-01T00:00:00.000Z",
        # "endDate": "2019-07-31T23:59:59.999Z",
        "startDate": startDate,
        "endDate": endDate,
        "me": "TEAM",
        "userGroupIds": [],
        "userIds": [],
        "projectIds": [],
        "clientIds": [],
        "taskIds": [],
        "tagIds": [],
        "billable": "BOTH",
        "includeTimeEntries": "true",
        "zoomLevel": "week",
        "description": "",
        "archived": "All",
        "roundingOn": "false"
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)
    response.encoding = 'utf-8'
    # print(response.text)
    rjs = response.json()
    projects = set()
    engineers = set()
    registers = []
    for entry in rjs['timeEntries']:
        username = entry['user']['name']
        description = entry['description']
        project = entry['project']['name']
        duration = hours_from_duration(entry['timeInterval']['duration'])
        # print("Description: {}\tUser: {}\tProject: {}\tDuration: {}h"
        #       .format(description, username, project, duration))
        # print(entry)
        projects.add(project)
        engineers.add(username)
        registers.append((project, username, duration))
    return projects, engineers, registers


def hours_from_duration(pt):
    duration = parse.DurationParser().parse(pt)
    return round(duration.get_seconds()//3600)

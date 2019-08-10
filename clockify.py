import json
import requests
import settings
import isodatetime.parsers as parse  # https://pypi.org/project/isodatetime/


base_url = "https://api.clockify.me/api"

headers = {
    "content-type": "application/json",
    "X-Api-Key": settings.API_KEY,
}

def get_workspaces():
    url = base_url + "/workspaces/"
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    # print(response.text)
    rj = response.json()
    print("numero de workspaces : {}".format(len(rj)))
    for entrada in rj:
        print(entrada)

def get_reports_summary():
    url = base_url + "/workspaces/{}/reports/summary/".format(settings.WORKSPACE_ID)
    data = {
        "startDate":"2019-07-01T00:00:00.000Z",
        "endDate": "2019-07-31T23:59:59.999Z",
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
    projects = {}
    people = {}
    for entry in rjs['timeEntries']:
        username = entry['user']['name']
        description = entry['description']
        project = entry['project'] ['name']
        duration = hours_from_duration(entry['timeInterval']['duration'])
        # print("Description: {}\tUser: {}\tProject: {}\tDuration: {}h"
        #       .format(description, username, project, duration))
        # print(entry)
        if username in people.keys():
            people[username] += duration
        else:
            people[username] = duration
        if project in projects.keys():
            projects[project] += duration
        else:
            projects[project] = duration
    # print(people)
    # print(projects)
    return people, projects




def hours_from_duration(pt):
    duration = parse.DurationParser().parse(pt)
    return round(duration.get_seconds()//3600)


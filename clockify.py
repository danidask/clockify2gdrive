import datetime
import json
import requests
import settings
import dateutil.parser
import isodatetime.parsers as isoparse  # https://pypi.org/project/isodatetime/
import pytz


base_url_api0 = "https://api.clockify.me/api"
base_url_api1 = "https://api.clockify.me/api/v1"

headers = {
    "content-type": "application/json",
    "X-Api-Key": settings.CLOCKIFY_API_KEY,
}

# API V0 ================================================================

def get_workspaces():
    url = base_url_api0 + "/workspaces/"
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    # print(response.text)
    rj = response.json()
    print("numero de workspaces : {}".format(len(rj)))
    for entrada in rj:
        print(entrada)


def get_engineers_ids():
    url = base_url_api0 + "/workspaces/{}/users".format(settings.CLOCKIFY_WORKSPACE_ID)
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    # print(response.text)
    rjs = response.json()
    engineers = {}
    for entry in rjs:
        if entry['status'] == "ACTIVE":
            engineers[entry['name']] = entry['id']
    return engineers  # {'Jhon Doe': '5c928a86536955400', 'Engineer1': '5d4d39c24e80e', 'Engineer2': '5d4d21663e2139'}

# API V1 ================================================================

def get_reports_summary(start, end, save_json=False):
    """ start and end -> datetime """
    # https://clockify.me/developers-api#operation--v1-workspaces--workspaceId--reports-summary-post
    url = "https://reports.api.clockify.me/v1/workspaces/{}/reports/detailed".format(settings.CLOCKIFY_WORKSPACE_ID)

    data = {
        "dateRangeStart": start.isoformat()+"Z",  # 2019-07-01T00:00:00.000Z
        "dateRangeEnd": end.isoformat()+"Z",
        "detailedFilter": {"page": 1, "pageSize": 200,},
        "exportType": "JSON",
        "rounding": False,
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    response.encoding = 'utf-8'
    # print(response.text)
    rjs = response.json()
    if save_json:
        with open('temp.json', 'w', encoding='utf-8') as f:
            json.dump(rjs, f, ensure_ascii=False, indent=4)
    # print(rjs)  # {'code': 401, 'message': 'Unauthorized'}
    projects = set()
    engineers = set()
    registers = []

    for entry in rjs['timeentries']:
        username = entry['userName']
        description = entry['description']
        date = entry['timeInterval']['start']  # 2019-07-18T09:06:00Z
        date = dateutil.parser.parse(date)  # datetime
        if not isinstance(entry['timeInterval']['duration'], int):
            continue  # duration is None when the clock is running, so ignore it
        # duration = hours_from_duration(entry['timeInterval']['duration'])
        duration = entry['timeInterval']['duration'] / 3600
        try:
            project = entry['projectName']
        except TypeError: #  TypeError: 'NoneType' object is not subscriptable
            continue
        # print("Description: {}\tUser: {}\tProject: {}\tDuration: {}h"
        #       .format(description, username, project, duration))
        # print(entry)
        projects.add(project)
        engineers.add(username)
        registers.append((project, username, duration, description, date))
    return list(projects), list(engineers), registers


def get_users():
    url = base_url_api1 + "/workspace/{}/users".format(settings.CLOCKIFY_WORKSPACE_ID)
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    # print(response.text)
    rjs = response.json()
    users = {}
    for entry in rjs:
        user_id = entry['id']
        name = entry['name']
        users[name] = user_id
    return users


def get_running_clock_user(userid):
    url = base_url_api1 + "/workspaces/{}/user/{}/time-entries".format(settings.CLOCKIFY_WORKSPACE_ID, userid)
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    # print(response.text)
    entries = response.json()
    for entry in entries:
        if entry['timeInterval']['end'] is None:  # clock active
            start = entry['timeInterval']['start']  # 2019-08-12T16:46:14Z
            start = dateutil.parser.parse(start)
            now = datetime.datetime.now(pytz.timezone('UTC'))
            time = now - start
            if time > datetime.timedelta(hours=settings.RUNNING_CLOCK_ALERT):
                return "You have a clock running for {} hours. Please save your work more often"\
                    .format(time.seconds//3600)
    return None


def hours_from_duration(pt):
    duration = isoparse.DurationParser().parse(pt)
    return duration.get_seconds()/3600

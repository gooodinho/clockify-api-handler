import requests
import json
import os

from dotenv import load_dotenv
from datetime import datetime, timedelta


load_dotenv()

api_key = os.getenv("API_KEY")
if len(api_key) == 0:
    raise(ValueError("API key is empty."))

data = {'x-api-key': api_key}

choice = input("Type 1 - to get all your time entries from active workspace\nType 2 - to get your report.\n\n")

if choice == '1' or choice == '2':
    data = {'x-api-key': api_key}
    user_info_response = requests.get('https://api.clockify.me/api/v1/user', headers=data)
    user_info_json = json.loads(user_info_response.content)
    user_id, workspace_id = user_info_json["id"], user_info_json["activeWorkspace"]

    if choice == '1':
        response = requests.get(f'https://api.clockify.me/api/v1/workspaces/{workspace_id}/user/{user_id}/time-entries', headers=data)
        json_response = json.loads(response.text)
        for num, entity in enumerate(json_response, start=1):
            print("------")
            print(f"Time entity №{num}")
            print("id: ", entity['id'])
            print("Description: ", entity['description'])
            print("project_id: ", entity['projectId'])
            print("Start time: ", entity['timeInterval']['start'])
            print("End time: ", entity['timeInterval']['end'])
            if entity['timeInterval']['duration'] is not None:
                print("Duration: ", entity['timeInterval']['duration'])
            else:
                print("Duration: ", "in progress")
            print("------")
    elif choice == '2':
        current_time = datetime.now().isoformat()
        body = {
            "dateRangeStart": "2022-09-01T00:00:00.000",
            "dateRangeEnd": current_time,
            "summaryFilter": {
                "groups": [
                    "DATE",
                    "TASK",
                    "TIMEENTRY"
                    ],
                },
            "exportType": "JSON"
            }

        response = requests.post(f'https://reports.api.clockify.me/v1/workspaces/{workspace_id}/reports/summary', headers=data, json=body)
        json_response = json.loads(response.text)

        print("Total time: ", str(timedelta(seconds=json_response['totals'][0]['totalTime'])))

        for group in json_response['groupOne']:
            print("------")
            print("Date: ", group['name'])
            print("Total duration: ", str(timedelta(seconds=group['duration'])))
            for num, child in enumerate(group['children'], start=1):
                print(f"Task №{num}")
                print("Name: ", child['name'])
                print("Time: ", str(timedelta(seconds=child['duration'])))
            print("------")

import requests
import json
import os

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")

data = {'x-api-key': api_key}
user_info_response = requests.get('https://api.clockify.me/api/v1/user', headers=data)
user_info_json = json.loads(user_info_response.content)

user_id, workspace_id = user_info_json["id"], user_info_json["activeWorkspace"]

r = requests.get(f'https://api.clockify.me/api/v1/workspaces/{workspace_id}/user/{user_id}/time-entries', headers=data)

print(json.dumps(r.json(), indent=2))
import requests
import os

api_token = os.environ["GITLAB_API_TOKEN"]

headers = {
    "PRIVATE-TOKEN": api_token
}
url = "https://gitlab.com/api/v4/projects/70726275/runners"

response = requests.get(url, headers=headers)

if response.status_code == 200:
    runners = response.json()
    for runner in runners:
        print(f"Runner ID: {runner['id']} - Description: {runner.get('description')}")
else:
    print(f"Fehler: {response.status_code} - {response.text}")
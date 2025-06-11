import requests
import os

class CoordinatorDaemon:
    def __init__(self):
        self.api_token = os.environ["GITLAB_API_TOKEN"]
        self.headers = {
            "PRIVATE-TOKEN": self.api_token
        }
        self.runners = []

    def fetch_runners(self):
        response = requests.get("https://gitlab.com/api/v4/projects/70726275/runners", headers=self.headers)

        if response.status_code == 200:
            runners = response.json()
            for runner in runners:
                print(runner)
                self.runners.append(runner)

        else:
            print(f"Fehler: {response.status_code} - {response.text}")

    def get_num_jobs_from_runner(self, runner_id):
        response = requests.get(f"https://gitlab.com/api/v4/runners/{runner_id}/jobs", headers=self.headers)
        out = []
        if response.status_code == 200:
            jobs = response.json()
            out = jobs
        else:
            print(f"Fehler: {response.status_code} - {response.text}")
        return out


cd = CoordinatorDaemon()
cd.fetch_runners()
for runner in cd.runners:
    jobs = cd.get_num_jobs_from_runner(runner["id"])
    print(f"Current number of jobs on {runner['id']}: {len(jobs)}")
import pprint

import requests
import os

class CoordinatorDaemon:
    def __init__(self):
        self.api_token = os.environ["GITLAB_API_TOKEN"]
        self.headers = {
            "PRIVATE-TOKEN": self.api_token
        }
        self.runner_ids = []
        self.runners = []
        self.fetch_runner_ids()

    def fetch_runner_ids(self):
        response = requests.get("https://gitlab.com/api/v4/projects/70726275/runners", headers=self.headers)

        if response.status_code == 200:
            runners = response.json()
            for runner in runners:
                self.runner_ids.append(runner["id"])

        else:
            print(f"Fehler: {response.status_code} - {response.text}")

    def get_runners(self):
        for rid in self.runner_ids:
            response = requests.get(f"https://gitlab.com/api/v4/runners/{rid}", headers=self.headers)
            self.runners.append(response.json())
        return self.runners

    def get_num_jobs(self, runner_id):
        response = requests.get(f"https://gitlab.com/api/v4/runners/{runner_id}/jobs", headers=self.headers)
        out = []
        if response.status_code == 200:
            jobs = response.json()
            for job in jobs:
                if job["status"] == "running":
                    out.append(job)
                #pprint.pprint(job)
        else:
            print(f"Error: {response.status_code} - {response.text}")
        return len(out)

    def get_vm_name(self, runner_id):
        for r in self.runners:
            if r["id"] == runner_id:
                for tag in r["tag_list"]:
                    s = tag.split(":")
                    if s[0] == "gcloud":
                        return s[1]
        return None

    def shutdown_vm(self, runner_id):
        import subprocess
        out = subprocess.run(["gcloud", "compute", "instances", "stop", self.get_vm_name(runner_id), "--zone=europe-west3-a"])
        out = str(out)
        print(out)


cd = CoordinatorDaemon()
for r in cd.get_runners():
    print(f"VM-name: {cd.get_vm_name(r['id'])}")
    print(f"Number of active jobs: {cd.get_num_jobs(r['id'])}")
    if cd.get_num_jobs(r["id"]) == 0 and cd.get_vm_name(r["id"]) is not None:
        print(f"No active jobs for {r['id']}. Shutting down {cd.get_vm_name(r['id'])}.")
        #cd.shutdown_vm(r["id"])
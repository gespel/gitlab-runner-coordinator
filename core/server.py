from dns.message import make_response
from flask import Flask, request, jsonify
import yaml
from core.gitlab_runner import GitlabRunner

class GitlabRunnerCoordinatorServer:
    def __init__(self, config_path, logger):
        self.configured_runners = []
        self.logger = logger
        self.config_path = config_path

        self.app = Flask(__name__)

        self._load_config()
        self._register_routes()

    def get_runner(self, name):
        for runner in self.configured_runners:
            if runner.name == name:
                return runner
        return None


    def _load_config(self):
        config = {}
        with open(self.config_path, "r") as f:
            config = yaml.safe_load(f.read())
            for r in config["runners"]:
                self.configured_runners.append(GitlabRunner(r["name"], r["address"]))

    def _register_routes(self):
        @self.app.route('/')
        def home():
            return jsonify({"info": "Please use /runners/<name> for runner status fetch"})

        @self.app.route('/runner/<name>/check', methods=['GET'])
        def check_runner(name):
            runner = self.get_runner(name)

            if runner is None:
                return jsonify({"message": "Runner not found"}), 500

            if runner.status == "stopped":
                self.logger.info(f"Starting {name}...")
                #TODO: Starting via gcloud cli
                runner.status = "starting"
                return jsonify({"status": runner.status, "message": "Runner off. Starting in progress."}), 200
            elif runner.status == "running":
                self.logger.info(f"Runner {name} already running.")
                return jsonify({"status": runner.status, "message": "Runner on. Complete."}), 200
            elif runner.status == "starting":
                self.logger.info(f"Request for starting runner {name}... Waiting for runner to start...")
                return jsonify({"status": runner.status, "message": "Runner starting. Waiting."}), 200


        @self.app.route('/runner/<name>', methods=['GET'])
        def get_runner(name):
            fetched_runner = None

            for runner in self.configured_runners:
                if runner.name == name:
                    fetched_runner = runner

            if fetched_runner is None:
                return jsonify({"message": "ERROR! runner NOT found"}), 500

            return jsonify(fetched_runner.to_dict())

        @self.app.route('/runner/<name>/status', methods=['GET'])
        def get_runner_status(name):
            fetched_runner = None

            for runner in self.configured_runners:
                if runner.name == name:
                    fetched_runner = runner

            if fetched_runner is None:
                return jsonify({"message": "ERROR! runner NOT found"}), 500

            return fetched_runner.to_dict()["status"], 200

        @self.app.route('/runner/<name>', methods=['POST'])
        def post_runner(name):
            data = request.get_json()

            if data["name"] is None:
                return jsonify({"message": "ERROR! You need to provide a name"}), 500

            if data["status"] is None:
                return jsonify({"message": "ERROR! You need to provide a status"}), 500

            r = self.get_runner(data["name"])
            if r is None:
                return jsonify({"message": "ERROR! Runner NOT found"})

            if data["status"] != "running" and data["status"] != "stopped" and data["status"] != "starting":
                return jsonify({"message": "ERROR! status must be 'running' or 'stopped' or 'starting'"})

            r.status = data["status"]

            return jsonify({"message": "OK"})

    def run(self):
        self.app.run(debug=True, port=5000)
from flask import Flask, request, jsonify
import yaml
from core.gitlab_runner import GitlabRunner

class GitlabRunnerCoordinatorServer:
    def __init__(self, config_path):
        self.configured_runners = []
        self.config_path = config_path

        self.app = Flask(__name__)

        self._load_config()
        self._register_routes()


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

        @self.app.route('/runner/<name>', methods=['GET'])
        def get_data(name):
            fetched_runner = None

            for runner in self.configured_runners:
                if runner.name == name:
                    fetched_runner = runner

            if fetched_runner is None:
                return jsonify({"status": "ERROR! runner NOT found"})

            return jsonify(fetched_runner.to_dict())


    def run(self):
        self.app.run(debug=True, port=5000)
from core.server import GitlabRunnerCoordinatorServer

grcs = GitlabRunnerCoordinatorServer("gitlab-runners.yaml")
grcs.run()
import logging
from core.server import GitlabRunnerCoordinatorServer

logger = logging.getLogger("GitlabRunnerCoordinator")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

grcs = GitlabRunnerCoordinatorServer("gitlab-runners.yaml", logger)
grcs.run()
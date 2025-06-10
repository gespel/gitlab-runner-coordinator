# Gitlab Runner Coordinator
The Gitlab Runner Coordinator is a solution designed to intelligently manage Google Cloud Compute instances, specifically configured as GitLab Runners. Its primary goal is to minimize their operational uptime, thereby significantly reducing cloud infrastructure costs and conserving energy.

This intelligent coordinator acts as a central control point, orchestrating the lifecycle of these compute instances. By dynamically starting runners only when CI/CD jobs are queued and stopping them once tasks are completed, it ensures that resources are consumed purely on demand. This approach moves away from the traditional model of continuously running runners, which often leads to wasted compute cycles and unnecessary expenditure.
## Usage:
`python coordinator.py`

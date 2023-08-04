import re
from typing import Protocol

from app.domain.job import Job
from app.domain.job_alert import JobAlert
from app.repository.alert_repository import JobAlertRepository


class JobAlertService(Protocol):
    """A protocol defining the contract for a job alert service.

    This protocol outlines the methods that a class should implement to function as a job alert service.

    """

    def get_job_alerts_to_notify(self, job: Job) -> list[JobAlert]:
        """Retrieve job alerts to notify based on a given job.

        This method should be implemented to fetch all job alerts from the service
        that match the given job and return them as a list of JobAlert objects.

        Args:
            job (Job): The Job object for which to find matching job alerts.

        Returns:
            List[JobAlert]: A list of JobAlert objects representing all the job alerts to be notified for the given job.

        """
        ...


class JobberwockyJobAlert:
    """An implementation of the JobAlertService protocol.

    This class provides methods to retrieve job alerts to notify based on a given job by matching job names with regular expressions.

    Attributes:
        repo (JobAlertRepository): The JobAlertRepository instance used to retrieve job alerts.

    """

    def __init__(self, job_alert_repository: JobAlertRepository):
        """Initialize the JobberwockyJobAlert.

        Args:
            job_alert_repository (JobAlertRepository): The JobAlertRepository instance used to retrieve job alerts.

        """
        self.repo = job_alert_repository

    def get_job_alerts_to_notify(self, job: Job) -> list[JobAlert]:
        """Retrieve job alerts to notify based on a given job.

        This method retrieves all job alerts from the repository and filters them based on regular expressions matching the given job's name.

        Args:
            job (Job): The Job object for which to find matching job alerts.

        Returns:
            List[JobAlert]: A list of JobAlert objects representing all the job alerts to be notified for the given job.

        """
        all_job_alert = self.repo.get_job_alerts()
        to_notify = []
        for job_alert in all_job_alert:
            if re.match(job_alert.regex_name, job.name):
                to_notify.append(job_alert)

        return to_notify

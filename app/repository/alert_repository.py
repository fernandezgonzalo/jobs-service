from typing import Protocol

from app.domain.job_alert import JobAlert
from app.storage import Storage


class JobAlertRepository(Protocol):
    """A protocol defining the contract for a job alert repository.

    This protocol outlines the methods that a class should implement to function as a job alert repository.

    """

    def __init__(self, storage: Storage):
        """Initialize the JobAlertRepository.

        Args:
            storage (Storage): An instance of Storage used to store job alerts.

        """
        ...

    def get_job_alerts(self) -> list[JobAlert]:
        """Retrieve job alerts from the repository.

        This method should be implemented to fetch all job alerts from the repository and return them as a list of JobAlert objects.

        Returns:
            List[JobAlert]: A list of JobAlert objects representing all the job alerts in the repository.

        """
        ...

    def add(self, alert_job: JobAlert):
        """Add a job alert to the repository.

        The job alert will be stored in the specified storage.

        Args:
            alert_job (JobAlert): The JobAlert object to be added.

        """
        ...


class InMemoryJobAlertRepository:
    """An implementation of the JobAlertRepository protocol using in-memory storage.

    This class provides methods to add and retrieve job alerts from an in-memory storage.

    Attributes:
        storage (Storage): The storage instance used to store job alerts in-memory.

    """

    def __init__(self, storage: Storage):
        """Initialize the InMemoryJobAlertRepository.

        Args:
            storage (Storage): An instance of Storage used to store job alerts in-memory.

        """
        self.storage = storage

    def get_job_alerts(self) -> list[JobAlert]:
        """Retrieve job alerts from the in-memory storage.

        Returns:
            List[JobAlert]: A list of JobAlert objects representing all the job alerts in the in-memory storage.

        """

        all_items = [JobAlert(**job_alert) for job_alert in self.storage.get_all()]

        return all_items

    def add(self, alert_job: JobAlert):
        """Add a job alert to the in-memory storage.

        The job alert will be stored in the in-memory storage.

        Args:
            alert_job (JobAlert): The JobAlert object to be added.

        """
        self.storage.add(alert_job.to_dict())

from typing import Protocol

from app.domain.job import Job
from app.storage import InMemoryStorage, Storage


class JobRepository(Protocol):
    """A protocol defining the contract for a job repository.

    This protocol outlines the methods that a class should implement to function as a job repository.

    """

    def __init__(self, storage: Storage):
        """Initialize the JobRepository.

        Args:
            storage (Storage): An instance of Storage used to store job data.

        """
        ...

    def add(self, job: Job):
        """Add a job to the repository.

        The job will be stored using the specified storage.

        Args:
            job (Job): The Job object to be added.

        """
        ...

    def get_jobs(self) -> list[Job]:
        """Retrieve all jobs from the repository.

        Returns:
            list[Job]: A list of Job objects representing all the jobs in the repository.

        """
        ...


class InMemoryJobRepository:
    """A repository to manage jobs using in-memory storage.

    This class provides methods to add and retrieve jobs from an in-memory storage.

    Attributes:
        storage (InMemoryStorage): An instance of InMemoryStorage used to store job data.

    """

    def __init__(self, storage: InMemoryStorage):
        """Initialize the InMemoryJobRepository.

        Args:
            storage (InMemoryStorage): An instance of InMemoryStorage used to store job data.

        """
        self.storage = storage

    def add(self, job: Job):
        """Add a job to the repository.

        The job will be stored in the in-memory storage.

        Args:
            job (Job): The Job object to be added.

        """
        self.storage.add(job.model_dump())

    def get_jobs(self) -> list[Job]:
        """Retrieve all jobs from the repository.

        Returns:
            list[Job]: A list of Job objects representing all the jobs in the repository.

        """
        all_items = [Job(**job) for job in self.storage.get_all()]

        return all_items

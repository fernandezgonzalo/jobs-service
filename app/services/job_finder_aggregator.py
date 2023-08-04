from typing import List, Protocol

from app.domain.job import Job


class JobFinderService(Protocol):
    """A protocol defining the contract for a job finder service.

    This protocol outlines the methods that a class should implement to function as a job finder service.

    """

    def get_jobs(self) -> [Job]:
        """Retrieve jobs from the job finder service.

        This method should be implemented to fetch jobs from the job finder service and return them as a list of Job objects.

        Returns:
            List[Job]: A list of Job objects representing the jobs found by the job finder service.

        """
        ...


class JobFinderAggregator:
    """A class to aggregate job data from multiple JobFinder services.

    This class takes a list of JobFinder services and aggregates job data from all of them.

    Attributes:
        job_finder_services (List[JobFinderService]): A list of JobFinder services to be aggregated.

    """

    def __init__(self, job_finder_services: List[JobFinderService]):
        """Initialize the JobFinderAgreggator.

        Args:
            job_finder_services (List[JobFinderService]): A list of JobFinder services to be aggregated.

        """
        self.job_finder_services = job_finder_services

    def get_jobs(self):
        """Aggregate job data from all JobFinder services.

        This method calls the get_jobs() method on each JobFinder service and aggregates all the job data into a single list.

        Returns:
            List[Job]: A list of Job objects representing all the aggregated jobs.

        """
        jobs = []
        for service in self.job_finder_services:
            try:
                service_jobs = service.get_jobs()
                jobs.extend(service_jobs)
            except Exception:
                pass

        return jobs

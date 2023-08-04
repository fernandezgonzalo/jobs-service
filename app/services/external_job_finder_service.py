from dataclasses import asdict, dataclass
from typing import Optional, Protocol
from urllib.parse import urljoin

import httpx


@dataclass
class JobFilters:
    name: Optional[str] = None
    salary_max: Optional[int] = None
    salary_min: Optional[int] = None
    country: Optional[str] = None


@dataclass
class Job:
    name: str
    salary: int
    country: str
    skills: [str]


class ExternalJobFinderService(Protocol):
    """A protocol defining the contract for an external job finder service.

    This protocol outlines the methods that a class should implement to function as an external job finder service.

    """

    def get_jobs(self, job_filters: JobFilters) -> [Job]:
        """Retrieve jobs from the external job finder service.

        This method should be implemented to fetch jobs based on the provided filters.

        Args:
            job_filters (JobFilters): An object representing filters to be applied while fetching jobs.

        Returns:
            List[Job]: A list of Job objects representing the jobs found by the external service.

        """
        ...


class JobFinderServiceError(Exception):
    """An exception class for errors related to the Job Finder Service.

    This class represents exceptions that may occur while using the Job Finder Service.

    Inherits from:
        Exception: The base class for all built-in exceptions.

    Example:
        try:
            # Code that may raise JobFinderServiceError
        except JobFinderServiceError as e:
            # Handle the exception here

    """

    pass


class JobberwockyExtraSource:
    """A class to interact with the Jobberwocky external source.

    This class provides methods to fetch job data from the Jobberwocky extra source service and convert it into Job objects.

    Attributes:
        service_url (str): The base URL of the Jobberwocky extra source service.

    """

    def __init__(self, service_url: str):
        """Initialize the JobberwockyExtraSource.

        Args:
            service_url (str): The base URL of the Jobberwocky extra source service.

        """
        self.service_url = service_url

    def _get(self, url: str, filters: Optional[JobFilters] = None) -> dict:
        """Send an HTTP GET request to the specified URL.

        This method sends an HTTP GET request to the provided URL and returns the response in JSON format.

        Args:
            url (str): The URL to send the GET request to.
            filters (Optional[JobFilters]): An optional object representing filters to apply to the request.

        Returns:
            dict: A dictionary representing the JSON response from the HTTP GET request.

        Raises:
            JobFinderServiceError: If an HTTP error occurs while making the request.

        """
        try:
            if filters:
                sanitized_filters = self._sanitize_filters(filters)
                response = httpx.get(url, sanitized_filters)
            else:
                response = httpx.get(url)
            return response.json()
        except httpx.HTTPError:
            raise JobFinderServiceError()

    def get_jobs(self, job_filters: Optional[JobFilters] = None) -> [Job]:
        """Retrieve jobs from the Jobberwocky extra source service.

        This method fetches job data from the Jobberwocky extra source service, applies optional filters, and converts the data into
        a list of Job objects.

        Args:
            job_filters (Optional[JobFilters]): An optional object representing filters to apply while fetching jobs.

        Returns:
            List[Job]: A list of Job objects representing the jobs fetched from the Jobberwocky service.

        """
        endpoint_name = "jobs"
        url = urljoin(self.service_url, endpoint_name)

        external_jobs = self._get(url, job_filters)

        jobs = []
        for job_row in external_jobs:
            job_name = job_row[0]
            job_salary = job_row[1]
            job_country = job_row[2]
            job_skills = job_row[3]
            job = Job(
                name=job_name, salary=job_salary, country=job_country, skills=job_skills
            )
            jobs.append(job)

        return jobs

    def _sanitize_filters(self, job_filters: JobFilters) -> dict:
        """Sanitize job filters.

        This method takes a JobFilters object and converts it into a dictionary, excluding any None values.

        Args:
            job_filters (JobFilters): The JobFilters object to sanitize.

        Returns:
            dict: A dictionary representing the sanitized filters.

        """
        filters = {
            filter_name: filter_value
            for filter_name, filter_value in asdict(job_filters).items()
            if filter_value is not None
        }

        return filters

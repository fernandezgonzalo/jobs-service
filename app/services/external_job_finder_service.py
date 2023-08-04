from typing import Protocol, Optional
from dataclasses import dataclass, asdict
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
    def get_jobs(self, job_filters: JobFilters) -> [Job]: ...


class JobFinderServiceError(Exception):
    pass


class JobberwockyExtraSource:
    def __init__(self, service_url: str):
        self.service_url = service_url

    def _get(self, url: str, filters: Optional[JobFilters] = None) -> dict:
        try:
            if filters:
                sanitized_filters = self._sanitize_filters(filters)
                response = httpx.get(url, filters)
            else:
                response = httpx.get(url)
            return response.json()
        except httpx.HTTPError as e:
            raise JobFinderServiceError()

    def get_jobs(self, job_filters: Optional[JobFilters] = None) -> [Job]:
        endpoint_name = "jobs"
        url = urljoin(self.service_url, endpoint_name)
        
        external_jobs = self._get(url, job_filters)

        jobs = []
        for job_row in external_jobs:
            job_name = job_row[0]
            job_salary = job_row[1]
            job_country = job_row[2]
            job_skills = job_row[3]
            job = Job(name=job_name, salary=job_salary, country=job_country, skills=job_skills)
            jobs.append(job)

        return jobs

    def _sanitize_filters(self, job_filters: JobFilters) -> dict:
        filters = {
            filter_name: filter_value for filter_name, filter_value in asdict(job_filters).items() if filter_value is not None
        }

        return filters
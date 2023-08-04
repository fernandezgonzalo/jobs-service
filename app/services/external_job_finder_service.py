from typing import Protocol, Optional
from dataclasses import dataclass, asdict, field
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


class JobberwockyExtraSource:
    def __init__(self, service_url: str):
        self.service_url = service_url

    def get_jobs(self, job_filters: Optional[JobFilters] = None) -> [Job]:
        endpoint_name = "jobs"
        url = urljoin(self.service_url, endpoint_name)
        
        if job_filters is not None:
            filters = self._sanitize_filters(job_filters)
            response = httpx.get(url, params=filters).json()
        else:
            response = httpx.get(url).json()

        jobs = []
        for job_row in response:
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
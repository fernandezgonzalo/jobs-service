from typing import Annotated

from fastapi import Depends, FastAPI

from app.dependencies import (
    get_alert_repository,
    get_job_alert_service,
    get_job_finder_aggregator,
    get_job_repository,
    get_notifier_service,
)
from app.domain.job import Job
from app.domain.job_alert import JobAlert
from app.repository.alert_repository import JobAlertRepository
from app.repository.repository import JobRepository
from app.services.external_job_finder_service import JobFinderServiceError
from app.services.job_alert import JobAlertService
from app.services.job_finder_aggregator import JobFinderAggregator
from app.services.notify_service import PrintEmailNotifier

from .schemas import JobAlertIn, JobAlertOut, JobIn, JobOut

app = FastAPI()


@app.post("/add-job", status_code=201, response_model=JobOut)
def add_new_job(
    new_job: JobIn,
    job_repository: Annotated[JobRepository, Depends(get_job_repository)],
    job_alert_service: Annotated[JobAlertService, Depends(get_job_alert_service)],
    notifier_service: Annotated[PrintEmailNotifier, Depends(get_notifier_service)],
):
    """Endpoint to add a new job to the repository.

    This endpoint allows clients to add a new job to the job repository. It expects a JobIn model representing
    the details of the new job. The job is added to the repository using the provided JobRepository instance.

    Args:
        new_job (JobIn): The JobIn model representing the details of the new job to be added.
        job_repository (JobRepository): The JobRepository instance used to store the jobs.

    Returns:
        JobOut: The JobOut model representing the added job.

    Raises:
        HTTPException: If there is an error while adding the job to the repository.

    Example:
        Request:
        POST /add-job
        {
            "name": "Software Engineer",
            "salary": 100000,
            "country": "USA",
            "skills": ["Python", "JavaScript", "Django"]
        }

        Response:
        {
            "name": "Software Engineer",
            "salary": 100000,
            "country": "USA",
            "skills": ["Python", "JavaScript", "Django"]
        }

    """
    job = Job(
        name=new_job.name,
        country=new_job.country,
        salary=new_job.salary,
        skills=new_job.skills,
    )
    job_repository.add(job)

    to_notify = job_alert_service.get_job_alerts_to_notify(job)
    for notification in to_notify:
        notifier_service.notify(notification.email, job)

    return new_job


@app.get("/jobs", response_model=list[JobOut])
def get_jobs(repository: Annotated[JobRepository, Depends(get_job_repository)]):
    """Endpoint to retrieve all jobs from the repository.

    This endpoint allows clients to fetch all the jobs from the job repository. It uses the provided JobRepository instance
    to retrieve the jobs and returns them as a list of JobOut models.

    Args:
        repository (JobRepository): The JobRepository instance used to fetch the jobs.

    Returns:
        list[JobOut]: A list of JobOut models representing all the jobs in the repository.

    Raises:
        HTTPException: If there is an error while fetching the jobs from the repository.

    Example:
    Request:
        GET /jobs

        Response:
        [
            {
                "name": "Software Engineer",
                "salary": 100000,
                "country": "USA",
                "skills": ["Python", "JavaScript", "Django"]
            },
            {
                "name": "Data Scientist",
                "salary": 90000,
                "country": "Canada",
                "skills": ["Python", "R", "Machine Learning"]
            },
            ...
        ]

    """
    jobs = repository.get_jobs()
    return jobs


@app.get("/aggregated-jobs", response_model=list[JobOut])
def aggregated_jobs(
    service: Annotated[JobFinderAggregator, Depends(get_job_finder_aggregator)],
):
    """Endpoint to retrieve aggregated jobs from multiple sources.

    This endpoint aggregates jobs from both the external job finder service and the job repository.
    It uses the provided ExternalJobFinderService instance to fetch jobs from the external service
    and the provided JobRepository instance to fetch jobs from the repository.

    Args:
        service (JobFinderAgreggator): The JobFinderAgreggator instance used to fetch jobs from the external services.

    Returns:
        list[JobOut]: A list of JobOut models representing all the aggregated jobs from both sources.

    Raises:
        HTTPException: If there is an error while fetching the jobs from the external service.

    Example:
    Request:
        GET /aggregated-jobs

        Response:
        [
            {
                "name": "Software Engineer",
                "salary": 100000,
                "country": "USA",
                "skills": ["Python", "JavaScript", "Django"]
            },
            {
                "name": "Data Scientist",
                "salary": 90000,
                "country": "Canada",
                "skills": ["Python", "R", "Machine Learning"]
            },
            ...
        ]

    """
    try:
        jobs = service.get_jobs()
    except JobFinderServiceError:
        jobs = []

    return jobs


@app.post("/job-alert", status_code=201, response_model=JobAlertOut)
def add_new_job_alert(
    job_alert: JobAlertIn,
    job_alert_repo: Annotated[JobAlertRepository, Depends(get_alert_repository)],
):
    new_job_alert = JobAlert(email=job_alert.email, regex_name=job_alert.regex_name)

    job_alert_repo.add(new_job_alert)

    return job_alert

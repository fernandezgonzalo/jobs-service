from typing import Annotated

from fastapi import Depends, FastAPI

from app.dependencies import get_external_job_finder_service, get_job_repository
from app.repository.repository import JobRepository
from app.services.external_job_finder_service import (
    ExternalJobFinderService,
    JobFinderServiceError,
)

from .schemas import JobIn, JobOut

app = FastAPI()


@app.post("/add-job", status_code=201, response_model=JobOut)
def add_new_job(
    new_job: JobIn, repository: Annotated[JobRepository, Depends(get_job_repository)]
):
    """Endpoint to add a new job to the repository.

    This endpoint allows clients to add a new job to the job repository. It expects a JobIn model representing
    the details of the new job. The job is added to the repository using the provided JobRepository instance.

    Args:
        new_job (JobIn): The JobIn model representing the details of the new job to be added.
        repository (JobRepository): The JobRepository instance used to store the jobs.

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
    repository.add(new_job)
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
    jobs = repository.get_all_jobs()
    return jobs


@app.get("/aggregated-jobs", response_model=list[JobOut])
def aggregated_jobs(
    service: Annotated[
        ExternalJobFinderService, Depends(get_external_job_finder_service)
    ],
    repository: Annotated[JobRepository, Depends(get_job_repository)],
):
    """Endpoint to retrieve aggregated jobs from multiple sources.

    This endpoint aggregates jobs from both the external job finder service and the job repository.
    It uses the provided ExternalJobFinderService instance to fetch jobs from the external service
    and the provided JobRepository instance to fetch jobs from the repository.

    Args:
        service (ExternalJobFinderService): The ExternalJobFinderService instance used to fetch jobs from the external service.
        repository (JobRepository): The JobRepository instance used to fetch jobs from the repository.

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
        extra_sources_jobs = service.get_jobs()
    except JobFinderServiceError:
        extra_sources_jobs = []
    jobs = repository.get_all_jobs()

    return jobs + extra_sources_jobs

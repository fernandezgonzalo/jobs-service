from fastapi import FastAPI, Depends
from typing import Annotated
from .schemas import JobIn, JobOut
from app.dependencies import get_external_job_finder_service
from app.dependencies import get_job_repository
from app.services.external_job_finder_service import ExternalJobFinderService
from app.repository.repository import JobRepository

import requests
from .settings import settings


app = FastAPI()


@app.post("/add-job", status_code=201, response_model=JobOut)
def add_new_job(new_job: JobIn, repository: Annotated[JobRepository, Depends(get_job_repository)]):
    repository.add(new_job)
    return new_job


@app.get("/jobs", response_model=list[JobOut])
def get_jobs(repository: Annotated[JobRepository, Depends(get_job_repository)]):
    jobs = repository.get_all_jobs()
    return jobs


@app.get("/aggregated-jobs", response_model=list[JobOut])
def agregated_jobs(
    service: Annotated[ExternalJobFinderService, Depends(get_external_job_finder_service)],
    repository: Annotated[JobRepository, Depends(get_job_repository)] 
):
    extra_sources_jobs = service.get_jobs()
    jobs = repository.get_all_jobs()

    return jobs + extra_sources_jobs
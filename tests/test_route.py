import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.repository.repository import InMemoryJobRepository
from app.dependencies import get_job_repository, get_external_job_finder_service
from app.storage import InMemoryStorage
from app.schemas import JobIn
from unittest.mock import MagicMock


# def get_job_repository_():
#     try:
#         memory_storage = InMemoryStorage()
#         job_repository = InMemoryJobRepository(memory_storage)
#         yield job_repository
#     finally:
#         memory_storage.clean()

# app.dependency_overrides[get_job_repository] = get_job_repository_

client = TestClient(app)


def test_add_new_job():
    new_job = {
        "name": "python dev",
        "country": "Arg",
        "skills": [],
        "salary": 1
    }

    response = client.post("/add-job", json=new_job)
    assert response.status_code == 201


def test_get_jobs_empty(fastapi_dep):
    repo = MagicMock()
    repo.get_all_jobs.return_value = []
    service = MagicMock()
    service.get_jobs.return_value = []

    with fastapi_dep(app).override(
        {
            get_job_repository: lambda: repo,
            get_external_job_finder_service: lambda: service
        }
    ):

        response = client.get("/jobs")
        assert response.status_code == 200
        assert response.json() == []


def test_get_jobs_non_empty(fastapi_dep):
    new_job = {
        "name": "python dev",
        "country": "Arg",
        "skills": [],
        "salary": 1
    }
    repo = MagicMock()
    repo.get_all_jobs.return_value = [new_job]
    service = MagicMock()
    service.get_jobs.return_value = []

    with fastapi_dep(app).override(
        {
            get_job_repository: lambda: repo,
            get_external_job_finder_service: lambda: service
        }
    ):
        response = client.get("/jobs")
        assert response.status_code == 200
        assert response.json() != []
        assert response.json() == [new_job]


def test_get_aggregated_jobs_empty_jobs(fastapi_dep):
    repo = MagicMock()
    repo.get_all_jobs.return_value = []
    service = MagicMock()
    service.get_jobs.return_value = []

    with fastapi_dep(app).override(
        {
            get_job_repository: lambda: repo,
            get_external_job_finder_service: lambda: service
        }
    ):
        response = client.get("/aggregated-jobs")
        assert response.status_code == 200
        assert response.json() == []


def test_get_aggregated_jobs_empty_repo(fastapi_dep):
    repo = MagicMock()
    repo.get_all_jobs.return_value = []
    service = MagicMock()
    mock_jobs = [
        {
            "name": "sr python",
            "salary": 1,
            "country": "arg",
            "skills": []
        }
    ]
    service.get_jobs.return_value = mock_jobs

    with fastapi_dep(app).override(
        {
            get_job_repository: lambda: repo,
            get_external_job_finder_service: lambda: service
        }
    ):
        response = client.get("/aggregated-jobs")
        assert response.status_code == 200
        assert response.json() == mock_jobs


def test_get_aggregated_jobs_empty_external_source(fastapi_dep):
    mock_jobs = [
        {
            "name": "sr python",
            "salary": 1,
            "country": "arg",
            "skills": []
        }
    ]
    repo = MagicMock()
    repo.get_all_jobs.return_value = mock_jobs

    service = MagicMock()
    service.get_jobs.return_value = []

    with fastapi_dep(app).override(
        {
            get_job_repository: lambda: repo,
            get_external_job_finder_service: lambda: service
        }
    ):
        response = client.get("/aggregated-jobs")
        assert response.status_code == 200
        assert response.json() == mock_jobs


def test_get_aggregated_job_not_empty(fastapi_dep):
    mock_jobs_repo = [
        {
            "name": "sr python",
            "salary": 1,
            "country": "arg",
            "skills": []
        }
    ]
    mock_jobs_service = [
        {
            "name": "ssr python",
            "salary": 2,
            "country": "arg",
            "skills": []
        }
    ]
    repo = MagicMock()
    repo.get_all_jobs.return_value = mock_jobs_repo

    service = MagicMock()
    service.get_jobs.return_value = mock_jobs_service

    with fastapi_dep(app).override(
        {
            get_job_repository: lambda: repo,
            get_external_job_finder_service: lambda: service
        }
    ):
        response = client.get("/aggregated-jobs")
        assert response.status_code == 200
        assert response.json() != []
        assert response.json() == mock_jobs_repo + mock_jobs_service
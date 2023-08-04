from app.services.external_job_finder_service import JobberwockyExtraSource, Job, JobFilters, JobFinderServiceError
from unittest.mock import patch

import httpx
import pytest

@pytest.fixture
def external_job_finder():
    service = JobberwockyExtraSource("http://test_url")

    return service


dummy_jobs = [
    ['Jr Java Developer', 24000, 'Argentina', ['Java', 'OOP']],
    ['SSr Java Developer', 34000, 'Argentina', ['Java', 'OOP', 'Design Patterns']],
    ['Sr Java Developer', 44000, 'Argentina', ['Java', 'OOP', 'Design Patterns']],
    ['Sr Developer', 44000, 'Argentina', ['PHP', 'OOP', 'Design Patterns']],
    ['Functional Analyst', 38000, 'Argentina', ['UX']],
    ['React Developer', 49000, 'Argentina', ['React', 'TypeScript']],
    ['Angular Developer', 49000, 'Argentina', ['Angular', 'TypeScript']],
    ['Database Administrator', 44000, 'Argentina', ['MySQL', 'Percona']],
    ['Windows server Admin', 44000, 'Argentina', ['Windows Server']],
    ['Sr UX Designer', 40000, 'Argentina', ['UX']],
    ['Jr C# Developer', 30000, 'Argentina', ['C#', 'OOP']],
    ['Ruby Developer', 34000, 'Argentina', ['Ruby', 'OOP']]
]

def test__get_without_filters(external_job_finder):
    filters = None

    with patch.object(httpx, "get") as mock_method:
        result = external_job_finder._get(url="test", filters=filters)
        mock_method.assert_called_with("test")


def test__get_with_filters(external_job_finder):
    filters = JobFilters(name="sr python")
    sanitized_filters = {
        "name": "sr python"
    }

    with patch.object(httpx, "get") as mock_method:
        result = external_job_finder._get(url="test", filters=filters)
        mock_method.assert_called_with("test", sanitized_filters)


def test__get_http_error(httpx_mock, external_job_finder):
    httpx_mock.add_exception(httpx.ReadTimeout("Unable to read within timeout"))

    with pytest.raises(JobFinderServiceError):
        external_job_finder._get(url="http://test", filters=None)


def test_get_jobs(external_job_finder):
    with patch.object(external_job_finder, "_get", return_value=dummy_jobs):
        jobs = external_job_finder.get_jobs()
        assert len(jobs) == len(dummy_jobs)
        assert all(isinstance(job, Job) for job in jobs)

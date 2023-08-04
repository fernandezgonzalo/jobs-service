import pytest

from app.storage import InMemoryStorage
from app.repository.repository import InMemoryJobRepository
from app.domain.job import Job


@pytest.fixture
def memory_storage():
    storage = InMemoryStorage()

    return storage


@pytest.fixture
def job_repo(memory_storage):
    repo = InMemoryJobRepository(memory_storage)

    return repo


def test_add_job(job_repo):
    new_job = Job(
        name="sr python",
        country="Arg",
        salary=10,
        skills=["python"]
    )

    job_repo.add(new_job)


def test_get_all_jobs_empty(job_repo):
    assert job_repo.get_all_jobs() == []


def test_get_all_jobs_not_empty(job_repo):
    new_job = Job(
        name="sr python",
        country="Arg",
        salary=10,
        skills=["python"]
    )

    job_repo.add(new_job)

    all_jobs = job_repo.get_all_jobs()
    assert all_jobs != []
    assert all_jobs[0] == new_job
import pytest

from app.storage import InMemoryStorage
from app.repository.alert_repository import InMemoryJobAlertRepository
from app.domain.job_alert import JobAlert

@pytest.fixture
def memory_storage():
    storage = InMemoryStorage()

    return storage

@pytest.fixture
def job_alert_repo(memory_storage):
    repo = InMemoryJobAlertRepository(memory_storage)

    return repo


def test_add_alert_job(job_alert_repo):
    new_alert_job = JobAlert(
        email="email1@gmail.com",
        regex_name="sr"
    )

    job_alert_repo.add(new_alert_job)


def test_get_job_alerts(job_alert_repo):

    
    alerts = [
        JobAlert(email="email1@gmail.com", regex_name="^sr"),
        JobAlert(email="email2@gmail.com", regex_name="^ssr"),
    ]
    for ja in alerts:
        job_alert_repo.add(ja)

    
    all_job_alerts = job_alert_repo.get_job_alerts()
    assert all_job_alerts != []
    assert all_job_alerts == alerts

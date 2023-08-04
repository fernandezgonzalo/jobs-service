import pytest

from app.services.job_alert import JobberwockyJobAlert
from app.repository.alert_repository import InMemoryJobAlertRepository
from app.storage import InMemoryStorage
from app.domain.job import Job
from app.domain.job_alert import JobAlert

from unittest.mock import patch

@pytest.fixture
def storage():
    storage = InMemoryStorage()
    
    return storage


@pytest.fixture
def repo(storage):
    repo = InMemoryJobAlertRepository(storage)

    return repo


@pytest.fixture
def job_alert(repo):
    job_alert = JobberwockyJobAlert(repo)

    return job_alert


def test_get_job_alerts_to_notify_empty_repo(job_alert):
    job = Job(
        name="sr python",
        country="arg",
        salary=1,
        skills=[]
    )
    to_notify = job_alert.get_job_alerts_to_notify(job)

    assert to_notify == []

def test_get_job_alerts_to_notify_no_empty_repo(job_alert):
    job = Job(
        name="sr python",
        country="arg",
        salary=1,
        skills=[]
    )
    alerts = [
        JobAlert(email="email1@gmail.com", regex_name="^sr"),
        JobAlert(email="email1@gmail.com", regex_name="^ssr"),
    ]
    with patch.object(job_alert.repo, "get_job_alerts", return_value=alerts) as mock_method:

        to_notify = job_alert.get_job_alerts_to_notify(job)
        mock_method.assert_called()
        assert to_notify == [JobAlert(email="email1@gmail.com", regex_name="^sr"),]
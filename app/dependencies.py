from app.repository.alert_repository import (
    InMemoryJobAlertRepository,
    JobAlertRepository,
)
from app.repository.repository import InMemoryJobRepository, JobRepository
from app.services.external_job_finder_service import (
    ExternalJobFinderService,
    JobberwockyExtraSource,
)
from app.services.job_alert import JobAlertService, JobberwockyJobAlert
from app.services.job_finder_aggregator import JobFinderAggregator
from app.services.notify_service import PrintEmailNotifier
from app.settings import settings
from app.storage import InMemoryStorage, Storage

# Initialize external_job_finder_service using JobberwockyExtraSource
external_job_finder_service: ExternalJobFinderService = JobberwockyExtraSource(
    service_url=settings.endpoint_extra_source_service
)

# Initialize memory_storage using InMemoryStorage
memory_storage: Storage = InMemoryStorage()
alert_memory_storage: Storage = InMemoryStorage()

# Initialize job_repository using InMemoryJobRepository
job_repository: JobRepository = InMemoryJobRepository(memory_storage)

# Initialize job_finder_agregator using JobFinderAggregator
job_finder_aggregator: JobFinderAggregator = JobFinderAggregator(
    [external_job_finder_service, job_repository]
)

# Initialize job_alert_repository using InMemoryJobalertRepository
job_alert_repository: JobAlertRepository = InMemoryJobAlertRepository(
    alert_memory_storage
)

# Initialize job_alert_service using JobberwockyJobalert
job_alert_service: JobAlertService = JobberwockyJobAlert(job_alert_repository)


# Initialize notifier Service
notifier = PrintEmailNotifier()


def get_notifier_service() -> PrintEmailNotifier:
    return notifier


def get_alert_repository() -> JobAlertRepository:
    """Retrieve the instance of the JobAlertRepository.

    Returns:
        JobAlertRepository: The instance of the JobAlertRepository.

    """
    return job_alert_repository


def get_job_alert_service() -> JobAlertService:
    """Retrieve the instance of the JobAlertService.

    Returns:
        JobAlertService: The instance of the JobAlertService.

    """
    return job_alert_service


def get_job_finder_aggregator() -> JobFinderAggregator:
    """Retrieve the instance of the JobFinderAggregator.

    Returns:
        JobFinderAggregator: The instance of the JobFinderAggregator.

    """
    return job_finder_aggregator


def get_external_job_finder_service() -> ExternalJobFinderService:
    """Retrieve the instance of the ExternalJobFinderService.

    Returns:
        ExternalJobFinderService: The instance of the ExternalJobFinderService.

    """
    return external_job_finder_service


def get_job_repository() -> JobRepository:
    """Retrieve the instance of the JobRepository.

    Returns:
        JobRepository: The instance of the JobRepository.

    """
    return job_repository

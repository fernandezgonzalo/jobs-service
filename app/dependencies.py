from app.repository.repository import InMemoryJobRepository, JobRepository
from app.services.external_job_finder_service import (
    ExternalJobFinderService,
    JobberwockyExtraSource,
)
from app.settings import settings
from app.storage import InMemoryStorage, Storage

# Initialize external_job_finder_service using JobberwockyExtraSource
external_job_finder_service: ExternalJobFinderService = JobberwockyExtraSource(
    service_url=settings.endpoint_extra_source_service
)

# Initialize memory_storage using InMemoryStorage
memory_storage: Storage = InMemoryStorage()

# Initialize job_repository using InMemoryJobRepository
job_repository: JobRepository = InMemoryJobRepository(storage=memory_storage)


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

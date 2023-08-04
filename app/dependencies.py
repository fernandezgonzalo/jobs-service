from app.services.external_job_finder_service import JobberwockyExtraSource, ExternalJobFinderService
from app.repository.repository import JobRepository, InMemoryJobRepository
from app.settings import settings
from app.storage import InMemoryStorage, Storage


external_job_finder_service: ExternalJobFinderService = JobberwockyExtraSource(
    service_url=settings.endpoint_extra_source_service
)

memory_storage: Storage = InMemoryStorage() 

job_repository: JobRepository = InMemoryJobRepository(
    storage=memory_storage
)

def get_external_job_finder_service() -> ExternalJobFinderService:
    return external_job_finder_service

def get_job_repository() -> JobRepository:
    return job_repository

from typing import Protocol
from app.storage import Storage, InMemoryStorage
from app.domain.job import Job
from app.storage import InMemoryStorage


class JobRepository:
    def __init__(self, storage: Storage):
        ...

    def add(self, job: Job):
        ...

    def get_all_jobs(self) -> list[Job]:
        ...


class InMemoryJobRepository:
    def __init__(self, storage: InMemoryStorage):
        self.storage = storage

    def add(self, job: Job):
        self.storage.add(job.model_dump())

    def get_all_jobs(self) -> list[Job]:
        all_items = [
            Job(**job) for job in self.storage.get_all()
        ]

        return all_items
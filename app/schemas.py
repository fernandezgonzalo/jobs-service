from pydantic import BaseModel, UUID4, NonNegativeInt


class Job(BaseModel):
    id: UUID4
    name: str
    country: str
    salary: NonNegativeInt
    skills: list[str]

class JobIn(BaseModel):
    name: str
    country: str
    salary: NonNegativeInt
    skills: list[str]

class JobOut(JobIn):
    pass
from pydantic import BaseModel, UUID4, NonNegativeInt


class JobIn(BaseModel):
    name: str
    country: str
    salary: NonNegativeInt
    skills: list[str]


class JobOut(JobIn):
    pass
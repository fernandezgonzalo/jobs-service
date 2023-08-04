from pydantic import BaseModel, NonNegativeInt


class JobIn(BaseModel):
    name: str
    country: str
    salary: NonNegativeInt
    skills: list[str]


class JobOut(JobIn):
    pass

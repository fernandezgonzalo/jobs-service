from pydantic import BaseModel, NonNegativeInt


class JobIn(BaseModel):
    name: str
    country: str
    salary: NonNegativeInt
    skills: list[str]


class JobOut(JobIn):
    pass


class JobAlertIn(BaseModel):
    email: str
    regex_name: str


class JobAlertOut(JobAlertIn):
    pass

from dataclasses import dataclass, asdict


class Dictable:
    def dict(self):
        return asdict(self)


@dataclass
class Job(Dictable):
    name: str
    country: str
    salary: int
    skills: list[str]


from dataclasses import asdict, dataclass


class Dictable:
    def to_dict(self):
        return asdict(self)


@dataclass
class Job(Dictable):
    name: str
    country: str
    salary: int
    skills: list[str]

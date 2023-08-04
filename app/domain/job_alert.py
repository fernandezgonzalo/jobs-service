from dataclasses import asdict, dataclass


class Dictable:
    def to_dict(self):
        return asdict(self)


@dataclass
class JobAlert(Dictable):
    email: str
    regex_name: str

from typing import Protocol


class Storage(Protocol):
    def add(self, item: dict): ...
    def clean(self): ...
    def get_all(self) -> list[dict]: ...


class InMemoryStorage:
    def __init__(self):
        self.storage = []

    def add(self, item: dict):
        self.storage.append(item)

    def clean(self):
        self.storage = []

    def get_all(self) -> list[dict]:
        return self.storage

from typing import Protocol


class Storage(Protocol):
    """A protocol defining the contract for a storage mechanism.

    This protocol outlines the methods that a class should implement to function as a storage mechanism.

    """

    def add(self, item: dict):
        """Add an item to the storage.

        Args:
            item (dict): A dictionary representing the item to be added to the storage.

        """
        ...

    def clean(self):
        """Clean the storage.

        This method should clear all the items from the storage.

        """
        ...

    def get_all(self) -> list[dict]:
        """Retrieve all items from the storage.

        Returns:
            list[dict]: A list of dictionaries representing all the items in the storage.

        """
        ...


class InMemoryStorage:
    """An implementation of the Storage protocol using in-memory storage.

    This class provides methods to add, clean, and retrieve items from an in-memory storage.

    Attributes:
        storage (list[dict]): The list to store the items in-memory.

    """

    def __init__(self):
        """Initialize the InMemoryStorage."""
        self.storage = []

    def add(self, item: dict):
        """Add an item to the in-memory storage.

        The item will be appended to the list representing the storage.

        Args:
            item (dict): A dictionary representing the item to be added to the storage.

        """
        self.storage.append(item)

    def clean(self):
        """Clean the in-memory storage.

        This method will clear all items from the list representing the storage.

        """
        self.storage = []

    def get_all(self) -> list[dict]:
        """Retrieve all items from the in-memory storage.

        Returns:
            list[dict]: A list of dictionaries representing all the items in the storage.

        """
        return self.storage

from app.storage import InMemoryStorage
import pytest


@pytest.fixture
def memory_storage():
    storage = InMemoryStorage()
    return storage


def test_init_storage(memory_storage):
    assert memory_storage.storage == []


def test_storage_add_item(memory_storage):
    item = {
        "name": "Pepe"
    }

    memory_storage.add(item)
    assert len(memory_storage.storage) == 1
    assert memory_storage.storage[0] == item


def test_storage_get_all_items_empty(memory_storage):
    assert memory_storage.get_all() == []


def test_storage_get_all_items_not_empty(memory_storage):
    items = [
        {"name": "Pepe"},
        {"name": "Carlos"}
    ]
    
    for item in items:
        memory_storage.add(item)

    items_saved = memory_storage.get_all()
    assert items_saved != []
    assert len(items_saved) == 2
    assert items_saved == items
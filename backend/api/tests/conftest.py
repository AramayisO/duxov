import pytest
from starlette.testclient import TestClient

from app.main import app
from app.storage.service import StorageService
from app.cache.service import CacheService


@pytest.fixture(scope="module")
def client():
    yield TestClient(app)


@pytest.fixture(scope="function")
def storage():
    yield StorageService


@pytest.fixture(scope="function")
def cache():
    yield CacheService

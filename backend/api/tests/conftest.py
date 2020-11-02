import pytest
from starlette.testclient import TestClient

from app.main import app
from app.storage.service import StorageService


@pytest.fixture(scope="module")
def client():
    yield TestClient(app)


@pytest.fixture(scope="module")
def storage():
    yield StorageService
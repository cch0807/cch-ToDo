import pytest

from todos.src.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    return TestClient(app=app)

import pytest
import uuid
from fastapi.testclient import TestClient

# from src.main import app
from endpoints.index import app

@pytest.fixture(scope="function")
def test_client():
    """ Create a test client. """

    with TestClient(app) as test_client:
        yield test_client

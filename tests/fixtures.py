import pytest
import requests

@pytest.fixture
def mock_request_exception(monkeypatch):
    """Mock `requests.request` to always raise a exception."""

    def mock_request(*args, **kwargs):
        raise Exception("Exception")

    monkeypatch.setattr(requests, "request", mock_request)


@pytest.fixture
def mock_request_timeout_exception(monkeypatch):
    """Mock `requests.request` to always raise timeout exception."""

    def mock_request(*args, **kwargs):
        raise requests.Timeout("Request timed out")

    monkeypatch.setattr(requests, "request", mock_request)

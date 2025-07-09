import pytest
import requests
from requests.exceptions import Timeout
# orginal
# from endpoints.index import app

# from .app import currency_service.fetch_exchange_rate  # Import from main code
# from . endpoints.index.app import currency_service  # Import from main code
from endpoints.index import app

#from app import fetch_exchange_rate

@pytest.mark.integration
def test_api_timeout_handling(monkeypatch):
    def mock_get(*args, **kwargs):
        raise Timeout("API timed out")
        raise Exception('This is the exception you expect to handle')

    monkeypatch.setattr(requests, "get", mock_get)

    result = app.price()  # Test the real function's behavior
    assert "error" in result
    assert result["error"] == "timeout"


def test_exchange_rate_endpoint_success(monkeypatch):
    def mock_fetch_exchange_rate():
        return ExchangeRateResponse(rates={"USD": 1.0, "EUR": 0.85})

    monkeypatch.setattr("app.currency_service.fetch_exchange_rate", mock_fetch_exchange_rate)

    response = client.get("/exchange-rate")
    assert response.status_code == 200
    assert response.json() == {"rates": {"USD": 1.0, "EUR": 0.85}}


def test_exchange_rate_endpoint_failure(monkeypatch):
    def mock_fetch_exchange_rate():
        return ErrorResponse(rates={"error": "timeout"})

    monkeypatch.setattr("my_app.currency_service.fetch_exchange_rate", mock_fetch_exchange_rate)

    response = client.get("/exchange-rate")
    assert response.status_code == 200
    assert response.json() == {"rates": {"error": "timeout"}}

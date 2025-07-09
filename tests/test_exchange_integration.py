import pytest

from my_app.models import ExchangeRateResponse, ErrorResponse

# pytest -m integration

@pytest.mark.integration
def test_fetch_exchange_rate_from_api():
    response = requests.get(API_URL)
    assert response.status_code == 200  # Ensure API call is successful
    data = response.json()
    # assert models
    assert "rates" in data  # Check expected structure
    assert "EUR" in data["rates"]  # Ensure a specific currency exists



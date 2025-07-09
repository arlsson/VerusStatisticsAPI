import time
import pytest


from models.block import ExchangeRateResult
from models.block import rpc_getinfo_blockcount_response


from .fixtures import mock_request_exception
from .fixtures import mock_request_timeout_exception


def test_healthcheck(test_client):
    response = test_client.get("/healthcheck")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}


# /blockcount

def test_blockcount_exception(test_client, mock_request_exception):

    response = test_client.get("/blockcount")
    assert response.json() == 'Error!!, success: False', f"blockcount rpc call general exception response isnt correct."
    assert response.status_code == 200,                  f"blockcount rpc call general exception status code isnt correct."


def test_blockcount_timeout_exception(test_client, mock_request_timeout_exception):

    response = test_client.get("/blockcount")
    assert response.json() == 'Error!!, success: False', f"blockcount rpc call general exception response isnt correct."
    assert response.status_code == 200,                  f"blockcount rpc call general exception status code isnt correct."


def test_blockcount(test_client):
    response = test_client.get("/blockcount")
    assert response.status_code == 200

    data  = response.text
    known = "3440058"

    assert int(data) > int(known),    f"upstream blockcount doesnt return isnt more than known latest. {data} < {known}"


# block

def test_price(test_client):

    for currency in ["usd", "eur"]:

        response = test_client.get(f"/price/{currency}")

        assert response.status_code == 200, f"response status from /price/{currency} is not 200."

        data  = response.json()

        expected_keys = {f"{currency}", f"{currency}_24h_change"}

        response_key = "verus-coin"

        assert response_key in data,                                  f"response is missing key {response_key}."

        for test_key in expected_keys:
            assert test_key in data[response_key],                    f"response is missing key {response_key}{test_key}."
            assert isinstance(data[response_key][test_key], float), f"{data[response_key][test_key]} is not Decimal, but '{type(data[response_key][test_key])}'"


    response = test_client.get(f"/price/nonexisting")

    assert response.status_code == 200, f"response status from /price/nonexisting is not 200."

    data  = response.json()

    assert response_key in data,     f"response is missing key {response_key}."
    assert data[response_key] == {}, f"response is not empty {data}."


def test_difficulty(test_client):
    response = test_client.get("/difficulty")
    assert response.status_code == 200

    number, suffix = response.json().split(" ") #"28.8 Trillion"
    assert False, f"failed."


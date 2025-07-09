from pydantic import BaseModel
from typing import Dict, Union

class ExchangeRateResponse(BaseModel):
    rates: Dict[str, float]

class ErrorResponse(BaseModel):
    rates: Dict[str, str]  # Example: {"error": "timeout"}

class Item(BaseModel):
    id: str
    title: str
    description: str | None = None

ExchangeRateResult = Union[ExchangeRateResponse, ErrorResponse]

rpc_getinfo_blockcount_response = str

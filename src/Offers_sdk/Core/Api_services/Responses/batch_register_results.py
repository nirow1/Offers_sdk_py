from typing import Optional
from dataclasses import dataclass
from src.Offers_sdk.Core.Api_services.Requests.register_product_request import RegisterProductRequest
from src.Offers_sdk.Core.Api_services.Responses.register_product_response import RegisterProductResponse

@dataclass
class BatchRegisterResult:
    product: RegisterProductRequest
    response: Optional[RegisterProductResponse] = None
    error: Optional[Exception] = None

from uuid import UUID

from pydantic import ValidationError
from Offers_sdk.Core.Errors.http_errors import HttpError
from Offers_sdk.Http_client.http_client import HttpClient
from Offers_sdk.Services.base_services_client import BaseServicesClient
from Offers_sdk.Core.Api_services.Responces.product_offers_response import ProductOffersResponse
from Offers_sdk.Core.Api_services.Requests.register_product_request import RegisterProductRequest
from Offers_sdk.Core.Api_services.Responces.register_product_response import RegisterProductResponse
from Offers_sdk.Core.Errors.Offers_api_errors.Offers_api_custom_errors import InvalidProductPayloadError
from Offers_sdk.Core.Errors.Product_service_errors.product_service_errors import (ProductServiceError,
                                                                                  UnauthorizedAccessError,
                                                                                  ProductAlreadyExistsError,
                                                                                  IdNotFoundError)
from Offers_sdk.Validation.schemas import RegisterProductSchema


class ProductsService(BaseServicesClient):
    def __init__(self, http_client: HttpClient):
        super().__init__(http_client)
        self._endpoint_base = "/api/v1/products"

    @property
    def endpoint_base(self) -> str:
        return self._endpoint_base

    async def register_product(self, bearer_token: str,
                               register_product_req: RegisterProductRequest,
                               ) -> RegisterProductResponse:
        try:
            validated = RegisterProductSchema.model_validate(register_product_req, strict=True)
            payload = validated.model_dump(mode='json')

            response = await self._http_client.request(bearer_token,
                                             f"{self.endpoint_base}/register",
                                             "POST",
                                             payload)
            return RegisterProductResponse(id=UUID(response["id"]))

        except ValidationError as e:
            raise InvalidProductPayloadError(f"Invalid product payload: {e}") from e

        except HttpError as  e:
            match e.status_code:
                case 401:
                    raise UnauthorizedAccessError(e.status_code, f"Unauthorized access when registering product") from e
                case 409:
                    raise ProductAlreadyExistsError(e.status_code, f"Product with the {register_product_req.id} already exists") from e
                case 422:
                    raise ProductServiceError(e.status_code, f"Product registration validation failed") from e
                case _:
                    raise ProductServiceError(e.status_code, f"Error registering product") from e

    async def get_product_offers(self, bearer_token: str,
                                 product_id: str) -> list[ProductOffersResponse]:
        url = f"{self.endpoint_base}/{product_id}/offers"

        try:
            response = await self._http_client.request(bearer_token, url, "GET")
        except HttpError as e:
            match e.status_code:
                case 401:
                    raise UnauthorizedAccessError(e.status_code, f"Unauthorized access when fetching offers for product {product_id}") from e
                case 404:
                    raise IdNotFoundError(e.status_code, f"Product with id {product_id} not found") from e
                case 422:
                    raise ProductServiceError(e.status_code, f"Product request validation failed {product_id}") from e
                case _:
                    raise ProductServiceError(e.status_code, f"Error fetching offers for product {product_id}") from e

        # Transform response into domain objects
        return [ProductOffersResponse.from_dict(item) for item in response]

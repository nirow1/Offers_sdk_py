from Offers_sdk.Core.Errors.http_errors import HttpError
from Offers_sdk.Http_client.http_client import HttpClient
from Offers_sdk.Services.base_services_client import BaseServicesClient
from Offers_sdk.Core.Api_services.Responces.product_offers_response import ProductOffersResponse
from Offers_sdk.Core.Api_services.Requests.register_product_request import RegisterProductRequest
from Offers_sdk.Core.Api_services.Responces.register_product_response import RegisterProductResponse
from Offers_sdk.Core.Errors.Product_service_errors.product_service_errors import (ProductServiceError,
                                                                                  UnauthorizedAccessError,
                                                                                  ProductAlreadyExistsError,
                                                                                  IdNotFoundError)


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
            return await self._http_client.request(bearer_token,
                                             f"{self.endpoint_base}/register",
                                             "POST",
                                             register_product_req)

        except HttpError as  e:
            if e.status_code == 401:
                raise UnauthorizedAccessError(401, f"Unauthorized access when registering product: {e.status_code}") from e
            elif e.status_code == 409:
                raise ProductAlreadyExistsError(409, f"Product with the {register_product_req.get('id')} already exists: {e.status_code}") from e
            elif e.status_code == 422:
                raise ProductServiceError(e.status_code, f"Product registration validation failed: {e.status_code}") from e
            else:
                raise ProductServiceError(e.status_code, f"Error registering product: {e}") from e

    async def get_product_offers(self, bearer_token: str,
                                 product_id: str) -> list[ProductOffersResponse]:
        url = f"{self.endpoint_base}/{product_id}/offers"

        try:
            response = await self._http_client.request(bearer_token, url, "GET")
        except HttpError as e:
            if e.status_code == 401:
                raise UnauthorizedAccessError(401, f"Unauthorized access when fetching offers for product {product_id}: {e.status_code}") from e
            elif e.status_code == 404:
                raise IdNotFoundError(404, f"Product with id {product_id} not found: {e.status_code}") from e
            elif e.status_code == 422:
                raise ProductServiceError(e.status_code, f"Product request validation failed {product_id}: {e.status_code}") from e
            else:
                raise ProductServiceError(e.status_code, f"Error fetching offers for product {product_id}: {e.status_code}") from e

        # Transform response into domain objects
        return [ProductOffersResponse.from_dict(item) for item in response]

from Http_client.http_client import HTTPClient
from Services.base_services_client import BaseServicesClient
from Core.Api_services.Requests.register_product_req import RegisterProductRequest
from Core.Api_services.Responces.product_offers_response import ProductOffersResponse
from Core.Api_services.Responces.register_product_response import RegisterProductResponse


class ProductsService(BaseServicesClient):
    def __init__(self, http_client: HTTPClient):
        super().__init__(http_client)
        self._endpoint_base = "/api/v1/products"

    @property
    def endpoint_base(self) -> str:
        return self._endpoint_base

    async def register_product(self, bearer_token: str,
                               register_product_req: RegisterProductRequest,
                               ) -> RegisterProductResponse:
        return await self._http_client.request(bearer_token,
                                         f"{self.endpoint_base}/register",
                                         "POST",
                                         register_product_req)

    async def get_product_offers(self, bearer_token: str,
                                 product_id: str
                                 ) -> ProductOffersResponse:
        return await self._http_client.request(bearer_token,
                                         f"{self.endpoint_base}/{product_id}/offers",
                                         "GET")
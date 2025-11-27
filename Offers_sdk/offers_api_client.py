import asyncio

from Offers_sdk.Core.Api_services.Requests.register_product_req import RegisterProductRequest
from Offers_sdk.Http_client.Implementations.aiohttp_client import AiohttpClient
from Offers_sdk.Services.Products.product_service import ProductsService
from Offers_sdk.Services.services_config import base_aiohttp_config
from Offers_sdk.Services.Products.auth_service import AuthService
from Offers_sdk.Validation.schemas import RegisterProductSchema
from Offers_sdk.Http_client.http_client import HTTPClient


class OffersApiClient:
    def __init__(self, http_client: HTTPClient | None = None):
        self.http_client = http_client if http_client is not None else AiohttpClient(**base_aiohttp_config)
        self._products_service: ProductsService= ProductsService(http_client)
        self._auth_service: AuthService= AuthService(http_client)

    async def register_product(self, product: RegisterProductRequest):
        request = await RegisterProductSchema.model_validate(product, strict=True)
        bearer_token = await self._auth_service.authenticate()
        return self._products_service.register_product(bearer_token, request)

    async def batch_register_products(self, products: list[RegisterProductRequest]):
        bearer_token = await self._auth_service.authenticate()

        tasks = [
            self._products_service.register_product(bearer_token, product)
            for product in products
        ]

        results = await asyncio.gather(*tasks)
        return results

    async def get_offers(self, product_id: str):
        bearer_token = await self._auth_service.authenticate()
        return self._products_service.get_product_offers(bearer_token, product_id)
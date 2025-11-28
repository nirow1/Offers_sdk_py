import asyncio
from multiprocessing.context import AuthenticationError

from pydantic import ValidationError

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
        self._products_service: ProductsService= ProductsService(self.http_client)
        self._auth_service: AuthService= AuthService(self.http_client)

    async def __aenter__(self):
        # If the http_client supports context management, enter it
        if hasattr(self.http_client, "__aenter__"):
            await self.http_client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if hasattr(self.http_client, "__aexit__"):
            await self.http_client.__aexit__(exc_type, exc, tb)

    async def register_product(self, product: RegisterProductRequest):
        try:
            validated = RegisterProductSchema.model_validate(product, strict=True)
            bearer_token = await self._auth_service.authenticate()
            payload = validated.model_dump(mode='json')
            return await self._products_service.register_product(bearer_token, payload)
        except ValidationError as e:
            raise ValueError(f"Invalid product payload: {e}") from e

        except AuthenticationError as e:
            raise RuntimeError(f"Authentication failed: {e}") from e

        except Exception as e:
            raise RuntimeError(f"Unexpected error in register_product: {e}") from e

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
        return await self._products_service.get_product_offers(bearer_token, product_id)
import uuid
import asyncio

from Offers_sdk.Http_client.http_client import HttpClient
from Offers_sdk.Services.Products.auth_service import AuthService
from Offers_sdk.Services.services_config import base_aiohttp_config
from Offers_sdk.Services.Products.product_service import ProductsService
from Offers_sdk.Http_client.Implementations.aiohttp_client import AiohttpClient
from Offers_sdk.Core.Api_services.Responces.register_product_response import RegisterProductResponse
from Offers_sdk.Core.Api_services.Requests.register_product_request import RegisterProductRequest
from Offers_sdk.Core.Errors.Authentication_errors.authentication_errors import AuthenticationError
from Offers_sdk.Core.Errors.Product_service_errors.product_service_errors import ProductServiceError
from Offers_sdk.Core.Errors.Offers_api_errors.Offers_api_custom_errors import (InvalidProductIdError,
                                                                               ProductOffersFetchError,
                                                                               ProductRegistrationError,
                                                                               ProductAuthenticationError)


class OffersApiClient:
    def __init__(self, http_client: HttpClient | None = None):
        self.http_client = http_client if http_client is not None else AiohttpClient(**base_aiohttp_config)
        self._products_service: ProductsService= ProductsService(self.http_client)
        self._auth_service: AuthService= AuthService(self.http_client)

    async def __aenter__(self):
        if hasattr(self.http_client, "__aenter__"):
            await self.http_client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if hasattr(self.http_client, "__aexit__"):
            await self.http_client.__aexit__(exc_type, exc, tb)

    async def register_product(self, product: RegisterProductRequest) -> RegisterProductResponse:
        """
            Registers a new product using the provided product details.

            Args:
                product (RegisterProductRequest): The product details to register.

            Returns:
                RegisterProductResponse: The response object from the product registration service.

            Raises:
                ProductAuthenticationError: If authentication fails during product registration.
                ProductRegistrationError: If the product service fails to register the product.
        """

        try:
            bearer_token = await self._auth_service.authenticate()
            return await self._products_service.register_product(bearer_token, product)

        except AuthenticationError as e:
            raise ProductAuthenticationError(f"{e.status_code}: Authentication failed during product registration: {e}") from e

        except ProductServiceError as e:
            raise ProductRegistrationError(f"{e.status_code}: Product service error during registration: {e}") from e

    async def batch_register_products(self, products: list[RegisterProductRequest]):
        bearer_token = await self._auth_service.authenticate()

        tasks = [
            self._products_service.register_product(bearer_token, product)
            for product in products
        ]

        results = await asyncio.gather(*tasks)
        return results

    async def get_offers(self, product_id: str):
        try:
            uuid.UUID(product_id, version=4)
        except ValueError:
            raise InvalidProductIdError(f": {product_id}")

        try:
            bearer_token = await self._auth_service.authenticate()
            return await self._products_service.get_product_offers(bearer_token, product_id)

        except AuthenticationError as e:
            raise ProductAuthenticationError(f"{e.status_code}: Authentication failed during fetching offers: {e}") from e

        except ProductServiceError as e:
            raise ProductOffersFetchError(f"{e.status_code}: Product service error during fetching offers: {e}") from e

        except Exception as e:
            raise Exception(f"Unexpected error in register_product: {e}") from e

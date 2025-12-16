import pytest

from uuid import UUID
from unittest.mock import AsyncMock
from src.Offers_sdk.Core.Errors.http_errors import HttpError
from src.Offers_sdk.Services.Products.product_service import ProductsService
from src.Offers_sdk.Core.Api_services.Responses.product_offers_response import ProductOffersResponse
from src.Offers_sdk.Core.Errors.Product_service_errors.product_service_errors import (ProductServiceError,
                                                                                      IdNotFoundError,
                                                                                      UnauthorizedAccessError)


@pytest.mark.asyncio
class TestGetProductOffers:
    def setup_method(self):
        self.client = AsyncMock()
        self.service = ProductsService(self.client)

    async def test_successful_fetch(self):
        # Mock response from HTTP client
        self.client.request.return_value = [
            {"id": str(UUID("550e8400-1429-41d4-a787-446655440000")), "price": 10, "items_in_stock": 5},
            {"id": str(UUID("9a7b330a-a736-4f05-bfef-3f0f379b6d19")), "price": 20, "items_in_stock": 5},
        ]

        result = await self.service.get_product_offers("token123", "product-uuid")
        assert isinstance(result, list)
        assert all(isinstance(item, ProductOffersResponse) for item in result)
        assert result[0].id == UUID("550e8400-1429-41d4-a787-446655440000")
        assert result[1].price == 20

    async def test_unauthorized_access_error(self):
        self.client.request.side_effect = HttpError(status_code=401)
        with pytest.raises(UnauthorizedAccessError):
            await self.service.get_product_offers("token123", "product-uuid")

    async def test_id_not_found_error(self):
        self.client.request.side_effect = HttpError(status_code=404)
        with pytest.raises(IdNotFoundError):
            await self.service.get_product_offers("token123", "product-uuid")

    async def test_validation_error(self):
        self.client.request.side_effect = HttpError(status_code=422)
        with pytest.raises(ProductServiceError):
            await self.service.get_product_offers("token123", "product-uuid")

    async def test_generic_error(self):
        self.client.request.side_effect = HttpError(status_code=500)
        with pytest.raises(ProductServiceError):
            await self.service.get_product_offers("token123", "product-uuid")
from uuid import UUID

import pytest
from unittest.mock import AsyncMock

from Offers_sdk.Core.Api_services.Requests.register_product_request import RegisterProductRequest
from Offers_sdk.Core.Errors.http_errors import HttpError
from Offers_sdk.Services.Products.product_service import ProductsService
from Offers_sdk.Core.Api_services.Responces.register_product_response import RegisterProductResponse
from Offers_sdk.Core.Errors.Product_service_errors.product_service_errors import (ProductServiceError,
                                                                                  UnauthorizedAccessError,
                                                                                  ProductAlreadyExistsError)


@pytest.mark.asyncio
class TestRegisterProduct:

    async def test_register_product_success(self):
        client = AsyncMock()
        client.request.return_value = RegisterProductResponse(id=UUID("550e890-1429c-41d4-a787-446655440000"))

        service = ProductsService(client)

        product = RegisterProductRequest(
            id=UUID("550e890-1429c-41d4-a787-446655440000"),
            name="Real Product",
            description="This is a real product"
        )

        response = await service.register_product("fake-token", product)

        assert isinstance(response, RegisterProductResponse)
        assert response.id == UUID("550e890-1429c-41d4-a787-446655440000")

    async def test_register_product_unauthorized(self):
        client = AsyncMock()
        client.request.side_effect = HttpError(401, "Unauthorized")

        service = ProductsService(client)

        request = RegisterProductRequest(id = UUID("550e890-1429c-41d4-a787-446655440000"),
                                         name="Test",
                                         description="Test desc")

        with pytest.raises(UnauthorizedAccessError) as exc:
            await service.register_product("fake-token", request)
        assert "Unauthorized access" in str(exc.value)

    async def test_register_product_conflict(self):
        client = AsyncMock()
        client.request.side_effect = HttpError(409, "Conflict")

        service = ProductsService(client)

        request = RegisterProductRequest(id=UUID("550e890-1429c-41d4-a787-446655440000"),
                                         name="Test",
                                         description="Test desc")

        with pytest.raises(ProductAlreadyExistsError) as exc:
            await service.register_product("fake-token", request)
        assert "already exists" in str(exc.value)

    async def test_register_product_validation_error(self):
        client = AsyncMock()
        client.request.side_effect = HttpError(422, "Validation failed")

        service = ProductsService(client)

        request = RegisterProductRequest(id=UUID("550e890-1429c-41d4-a787-446655440000"),
                                         name=222,
                                         description="Test desc")

        with pytest.raises(ProductServiceError) as exc:
            await service.register_product("fake-token", request)
        assert "validation failed" in str(exc.value)

    async def test_register_product_unexpected_error(self):
        client = AsyncMock()
        client.request.side_effect = HttpError(500, "Internal Server Error")

        service = ProductsService(client)

        request = RegisterProductRequest(id=UUID("550e890-1429c-41d4-a787-446655440000"),
                                         name="Test",
                                         description="Test desc")
        
        with pytest.raises(ProductServiceError) as exc:
            await service.register_product("fake-token", request)
        assert "Error registering product" in str(exc.value)
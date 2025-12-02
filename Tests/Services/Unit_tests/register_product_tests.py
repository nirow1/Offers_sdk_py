import pytest
from unittest.mock import AsyncMock
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
        client.request.return_value = {"id": "123", "name": "Demo Product"}

        service = ProductsService()
        service._http_client = client

        req = {"id": "123", "name": "Demo Product"}
        response = await service.register_product("fake-token", req)

        assert isinstance(response, RegisterProductResponse)
        assert response.get("id") == "123"

    async def test_register_product_unauthorized(self):
        client = AsyncMock()
        client.request.side_effect = HttpError(401, "Unauthorized")

        service = ProductsService()
        service._http_client = client

        req = {"id": "123"}
        with pytest.raises(UnauthorizedAccessError) as exc:
            await service.register_product("fake-token", req)
        assert "Unauthorized access" in str(exc.value)

    async def test_register_product_conflict(self):
        client = AsyncMock()
        client.request.side_effect = HttpError(409, "Conflict")

        service = ProductsService()
        service._http_client = client

        req = {"id": "123"}
        with pytest.raises(ProductAlreadyExistsError) as exc:
            await service.register_product("fake-token", req)
        assert "already exists" in str(exc.value)

    async def test_register_product_validation_error(self):
        client = AsyncMock()
        client.request.side_effect = HttpError(422, "Validation failed")

        service = ProductsService()
        service._http_client = client

        req = {"id": "123"}
        with pytest.raises(ProductServiceError) as exc:
            await service.register_product("fake-token", req)
        assert "validation failed" in str(exc.value)

    async def test_register_product_unexpected_error(self):
        client = AsyncMock()
        client.request.side_effect = HttpError(500, "Internal Server Error")

        service = ProductsService()
        service._http_client = client

        req = {"id": "123"}
        with pytest.raises(ProductServiceError) as exc:
            await service.register_product("fake-token", req)
        assert "Error registering product" in str(exc.value)
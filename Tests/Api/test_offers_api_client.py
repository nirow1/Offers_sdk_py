import pytest

from uuid import UUID
from dotenv import load_dotenv
from Offers_sdk.offers_api_client import OffersApiClient
from Offers_sdk.Http_client.http_client import HTTPClient

# --- Fakes for testing ---
class FakeHttpClient(HTTPClient):
    async def _fetch_data(self, bearer_token, endpoint, method, data=None):
        # Always return a predictable response
        return {"status": "ok"}

class FakeAuthService:
    async def authenticate(self):
        # Return a fake token without hitting a real API
        return "fake-token"

@pytest.mark.asyncio
async def test_register_product_validates_schema():
    load_dotenv()

    product = {
        "id": UUID("550e8400-e29b-41d4-a716-446655440000"),
        "name": "Test",
        "description": "Desc"
    }

    fake_http = FakeHttpClient()
    fake_auth = FakeAuthService()

    async with OffersApiClient(http_client=fake_http) as client:
        # override the real auth service
        client._auth_service = fake_auth

        result = await client.register_product(product)

    assert result == {"status": "ok"}

async def test_register_product_validates_schema_fail():
    load_dotenv()

    product = {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "Test",
        "description": "Desc"
    }

    fake_http = FakeHttpClient()
    async with OffersApiClient(http_client=fake_http) as client:
        with pytest.raises(ValueError):
            await client.register_product(product)

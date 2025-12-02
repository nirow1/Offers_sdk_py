from uuid import UUID

import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer
from Offers_sdk.Http_client.Implementations.aiohttp_client import AiohttpClient
from Offers_sdk.Services.Products.product_service import ProductsService
from Offers_sdk.Core.Api_services.Responces.product_offers_response import ProductOffersResponse


# --- Shared handler ---
async def offers_handler(request):
    product_id = request.match_info["product_id"]
    print(f"Handler called for product_id={product_id}")
    return web.json_response([
        {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "price": 100,
            "items_in_stock": 5
        },
        {
            "id": "123e4967-e85b-12d5-a456-426b14c75000",
            "price": 103,
            "items_in_stock": 4
        }
    ])

# --- Fixture to spin up fake server ---
@pytest.fixture
async def fake_server():
    app = web.Application()
    app.router.add_get("/api/v1/products/{product_id}/offers", offers_handler)

    server = TestServer(app)
    client = TestClient(server)
    await client.start_server()

    try:
        yield client
    finally:
        await client.close()
        await server.close()

# --- Parametrized test ---
@pytest.mark.asyncio
@pytest.mark.parametrize("product_id,expected", [
    ("product123", [
        (UUID("123e4567-e89b-12d3-a456-426614174000"), 100, 5),
        (UUID("123e4967-e85b-12d5-a456-426b14c75000"), 103, 4),
    ]),
])
async def test_get_product_offers_success(fake_server, product_id, expected):
    base_url = str(fake_server.make_url("")).rstrip("/")
    async with AiohttpClient(base_url=base_url) as http_client:
        service = ProductsService(http_client)
        result = await service.get_product_offers("fake_token", product_id)

    # Compare results in a clean loop
    for offer, (exp_id, exp_price, exp_stock) in zip(result, expected):
        assert isinstance(offer, ProductOffersResponse)
        assert offer.id == exp_id
        assert offer.price == exp_price
        assert offer.items_in_stock == exp_stock
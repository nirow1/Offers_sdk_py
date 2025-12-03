from uuid import UUID
from aiohttp import web
from pygments.lexers import data
from Tests.fake_server import FakeServer
from Offers_sdk.Validation.schemas import RegisterProductSchema
from Offers_sdk.Services.Products.product_service import ProductsService
from Offers_sdk.Http_client.Implementations.aiohttp_client import AiohttpClient
from Offers_sdk.Core.Api_services.Requests.register_product_request import RegisterProductRequest
from Offers_sdk.Core.Api_services.Responces.register_product_response import RegisterProductResponse

async def offers_handler(request):
    data = await request.json()
    # Return the expected API response
    return web.json_response({
        "id": data["id"]  # echo back the id
    })

async def test_get_product_offers_success():
    server = FakeServer()
    server.add_route("POST", "/api/v1/products/register", offers_handler)
    await server.start()

    product = RegisterProductRequest(
        id=UUID("550e890-1429c-41d4-a787-446855440500"),
        name="Real Product",
        description="This is a real product"
    )

    try:
        async with AiohttpClient(base_url=server.base_url) as http_client:
            service = ProductsService(http_client)
            result = await service.register_product("fake_token", product)

            assert isinstance(result, RegisterProductResponse)
            assert result.id == product.id
    finally:
        await server.close()
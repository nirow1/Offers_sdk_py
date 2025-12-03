import pytest

from aiohttp import web
from dotenv import load_dotenv
from Tests.fake_server import FakeServer
from Offers_sdk.Services.Products.auth_service import AuthService
from Offers_sdk.Core.Api_services.Responces.auth_response import AuthResponse
from Offers_sdk.Http_client.Implementations.aiohttp_client import AiohttpClient


async def authentication_handler(request):
    return web.json_response({"access_token": "fake_access_token_12345"})

@pytest.mark.asyncio
async def test_authenticate():
    load_dotenv()
    server = FakeServer()
    server.add_route("POST", "/api/v1/auth", authentication_handler)
    await server.start()

    try:
        async with AiohttpClient(base_url=server.base_url) as http_client:
            service = AuthService(http_client)
            response = await service.authenticate()

            auth_response = AuthResponse(access_token=response)

            assert auth_response.access_token == "fake_access_token_12345"
    finally:
        await server.close()
from aiohttp import web
from aiohttp.test_utils import TestServer, TestClient

class FakeServer:
    def __init__(self, app_factory=None):
        # Allow passing a custom app factory, default to empty app
        self.app = app_factory() if app_factory else web.Application()
        self._server = None
        self._client = None

    async def start(self):
        self._server = TestServer(self.app)
        self._client = TestClient(self._server)
        await self._client.start_server()
        return self

    async def close(self):
        if self._client:
            await self._client.close()
        if self._server:
            await self._server.close()

    @property
    def base_url(self) -> str:
        return str(self._client.make_url("")).rstrip("/")

    def add_route(self, method: str, path: str, handler):
        self.app.router.add_route(method, path, handler)
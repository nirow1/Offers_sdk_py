from Http_client.http_client import HTTPClient, U, T
from Core.Errors.http_errors import HTTPError
from typing import Literal, Optional

import aiohttp


class AiohttpClient(HTTPClient):
    def __init__(self):
        super().__init__()
        self._session: aiohttp.ClientSession | None = None

    async def __aenter__(self):
        # Create session when entering context
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        # Ensure session is closed when exiting context
        if self._session:
            await self._session.close()

    async def _fetch_data(self,
                         bearer_token: str,
                         endpoint: str,
                         method: Literal["GET", "POST"],
                         data: Optional[U] | None = None
                         ) -> T:
        headers = {"Authorization": f"Bearer {bearer_token}"}
        url = f"{self._base_url}{endpoint}"

        async with self._session.request(method, url, headers=headers, json=data) as response:
            response.raise_for_status()
            return await response.json() # Await as aiohttp response.json() is a coroutine

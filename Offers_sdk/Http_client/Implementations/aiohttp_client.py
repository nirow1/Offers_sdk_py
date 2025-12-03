import aiohttp

from typing import Literal, Optional, Any
from Offers_sdk.Http_client.http_client import HttpClient, U, T


class AiohttpClient(HttpClient):
    def __init__(self, base_url: str | None = None, **session_kwargs: Any):
        super().__init__(base_url=base_url)
        self._session: Optional[aiohttp.ClientSession] = None
        self._session_kwargs = session_kwargs

    async def __aenter__(self):
        # Create session when entering context
        self._session = aiohttp.ClientSession(**self._session_kwargs)
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
        headers = {"Bearer": bearer_token}
        url = f"{self._base_url}{endpoint}"

        async with self._session.request(method, url, headers=headers, json=data) as response:
            response.raise_for_status()
            return await response.json() # Await as aiohttp response.json() is a coroutine

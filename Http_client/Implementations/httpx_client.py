from Http_client.http_client import HTTPClient, U, T
from typing import Literal

import httpx


class HTTPXClient(HTTPClient):
    def __init__(self):
        super().__init__()
        self._client: httpx.AsyncClient = httpx.AsyncClient()

    async def _fetch_data(self,
                            bearer_token: str,
                            endpoint: str,
                            method: Literal["GET", "POST"],
                            data: U | None = None
                            ) -> T:
        headers = {"Authorization": f"Bearer {bearer_token}"}
        url = f"{self._base_url}{endpoint}"

        response = await self._client.request(method, url, headers=headers, json=data)
        response.raise_for_status()
        return response.json() # no await needed here as httpx response.json() is not a coroutine

    async def close(self):
        await self._client.aclose()
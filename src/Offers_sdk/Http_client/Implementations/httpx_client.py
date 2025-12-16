from src.Offers_sdk.Http_client.http_client import HttpClient, U, T
from typing import Literal

import httpx


class HttpxClient(HttpClient):
    def __init__(self,  base_url: str | None = None, **client_kwargs):
        super().__init__(base_url=base_url)
        self._client: httpx.AsyncClient = httpx.AsyncClient(**client_kwargs)

    async def __aenter__(self):
        await self._client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._client.__aexit__(exc_type, exc, tb)

    async def _fetch_data(
        self,
        bearer_token: str,
        endpoint: str,
        method: Literal["GET", "POST"],
        data: U | None = None) -> T:
        url = f"{self._base_url}{endpoint}"
        headers = {"Bearer": f" {bearer_token}"}
        response = await self._client.request(method, url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()  # synchronous in httpx
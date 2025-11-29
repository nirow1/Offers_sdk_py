import asyncio
import os

from Offers_sdk.Core.Errors.http_errors import HTTPError
from typing import TypeVar, Literal
from abc import ABC, abstractmethod

T = TypeVar('T')
U = TypeVar('U')

class HttpClient(ABC):
    def __init__(self,
                 base_url: str | None = None,
                 max_retries: int | None = None) -> None:
        self._base_url: str = base_url or os.environ.get("API_BASE_URL", "")
        self._max_retries: int = max_retries or int(os.environ.get("MAX_API_REQUEST_RETRIES", "3"))

    async def request(self,
                      bearer_token: str,
                      endpoint: str,
                      method: Literal["GET", "POST"],
                      data: U | None = None) -> T:
        last_error: Exception | None = None

        for attempt in range(1, self._max_retries + 1):
            try:
                return await self._fetch_data(bearer_token, endpoint, method, data)
            except Exception as e:
                last_error = e

                if attempt < self._max_retries:
                    await asyncio.sleep((2 ** (attempt - 1)))

        raise HTTPError(
            500,
            f"Failed to fetch data after {self._max_retries} attempts: {last_error}",
            last_error)

    @abstractmethod
    async def _fetch_data(self,
                         bearer_token: str,
                         endpoint: str,
                         method: Literal["GET", "POST"],
                         data: U | None = None) -> T:
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc, tb):
        ...
import asyncio
import os

from Offers_sdk.Core.Errors.http_errors import HTTPError
from typing import TypeVar, Literal
from abc import ABC, abstractmethod

T = TypeVar('T')
U = TypeVar('U')

class HTTPClient(ABC):
    def __init__(self) -> None:
        self._max_retries: int = int(os.environ["MAX_API_REQUEST_RETRIES"])
        self._base_url: str = "http://localhost:8000"

    async def request(self,
                      bearer_token: str,
                      endpoint: str,
                      method: Literal["GET", "POST"],
                      data: U | None = None
                      ) -> T:
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
                         data: U | None = None
                         ) -> T:
        pass
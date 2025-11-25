from Http_client.http_client import HTTPClient
from typing import Literal, TypeVar

import requests

T = TypeVar('T')
U = TypeVar('U')


class RequestsClient(HTTPClient):
    async def _fetch_data(self,
                         bearer_token: str,
                         endpoint: str,
                         method: Literal["GET", "POST"],
                         data: U | None = None
                         ) -> T:
        pass
from Offers_sdk.Http_client.http_client import HTTPClient, U, T
from typing import Literal

import requests


class RequestsClient(HTTPClient):
    def __init__(self):
        super().__init__()
        self._session: requests.Session = requests.Session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self._session.close()

    def _fetch_data(self,
                         bearer_token: str,
                         endpoint: str,
                         method: Literal["GET", "POST"],
                         data: U | None = None
                         ) -> T:
        headers = {"Authorization": f"Bearer {bearer_token}"}
        url = f"{self._base_url}{endpoint}"

        response = self._session.request(method, url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
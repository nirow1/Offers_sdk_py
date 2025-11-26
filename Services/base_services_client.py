from abc import ABC, abstractmethod

from Http_client.http_client import HTTPClient


class BaseServicesClient(ABC):
    def __init__(self, http_client: HTTPClient):
        self._http_client: HTTPClient = http_client

    @property
    @abstractmethod
    def endpoint_base(self) -> str:
        pass
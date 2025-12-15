from abc import ABC, abstractmethod

from src.Offers_sdk.Http_client.http_client import HttpClient


class BaseServicesClient(ABC):
    def __init__(self, http_client: HttpClient):
        self._http_client: HttpClient = http_client

    @property
    @abstractmethod
    def endpoint_base(self) -> str:
        pass
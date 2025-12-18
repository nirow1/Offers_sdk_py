import os

from typing import Optional
from datetime import datetime, timedelta
from src.Offers_sdk.Core.Errors.http_errors import HttpError
from src.Offers_sdk.Core.Infrastructure.token_catch import TokenCache
from src.Offers_sdk.Services.base_services_client import BaseServicesClient
from src.Offers_sdk.Core.Api_services.Responses.auth_response import AuthResponse
from src.Offers_sdk.Core.Errors.Authentication_errors.authentication_errors import (AuthenticationError, BadAuthRequestError,
                                                                                    InvalidCredentialsError)


class AuthService(BaseServicesClient):
    def __init__(self, http_client):
        super().__init__(http_client)

        self._refresh_token: str = os.environ["REFRESH_TOKEN"]
        self._access_token: Optional[str] = None
        self._access_token_expiration: Optional[datetime] = None
        self._token_cache: TokenCache = TokenCache()
        self._endpoint_base: str = "/api/v1/auth"

    @property
    def endpoint_base(self) -> str:
        return self._endpoint_base

    async def authenticate(self) -> str:
        if  self._is_access_token_valid() or self._does_token_exist():
            assert self._access_token is not None
            return self._access_token

        try:
            raw = await self._http_client.request(bearer_token=self._refresh_token,
                                                                     endpoint=self._endpoint_base,
                                                                     method="POST",
                                                                     data=None)
            response = AuthResponse(**raw)

        except HttpError as e:
            match e.status_code:
                case 400:
                    raise BadAuthRequestError(e.status_code,f"Malformed authentication request: refresh token is invalid or unusable") from e
                case 401:
                    raise InvalidCredentialsError(e.status_code,f"Invalid credentials or expired token") from e
                case 422:
                    raise AuthenticationError(e.status_code,f"Authentication request validation failed") from e
                case _:
                    raise AuthenticationError(e.status_code, f"Authentication failed") from e

        self._access_token = response.access_token
        self._access_token_expiration = datetime.now() + timedelta(minutes=5)
        self._token_cache.save(self._access_token, self._access_token_expiration)
        return self._access_token

    def _does_token_exist(self) -> bool:
        cached_token = self._token_cache.load()
        if cached_token:
            token, expiration = cached_token
            self._access_token = token
            self._access_token_expiration = expiration
            return True
        return False

    def _is_access_token_valid(self) -> bool:
        return (self._access_token is not None
                and self._access_token_expiration is not None
                and datetime.now() < self._access_token_expiration)
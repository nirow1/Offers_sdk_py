import os

from typing import Optional
from datetime import datetime, timedelta
from Offers_sdk.Core.Errors.http_errors import HttpError
from Offers_sdk.Services.base_services_client import BaseServicesClient
from Offers_sdk.Core.Api_services.Responces.auth_response import AuthResponse
from Offers_sdk.Core.Errors.Authentication_errors.authentication_errors import (AuthenticationError, BadAuthRequestError,
                                                                                InvalidCredentialsError)


class AuthService(BaseServicesClient):
    def __init__(self, http_client):
        super().__init__(http_client)

        self._refresh_token: str = os.environ["REFRESH_TOKEN"]
        self._access_token: Optional[str] = None
        self._access_token_expiration: Optional[datetime] = None
        self._endpoint_base: str = "/api/v1/auth"

    @property
    def endpoint_base(self) -> str:
        return self._endpoint_base

    async def authenticate(self) -> str:
        if self._is_access_token_valid():
            assert self._access_token is not None
            return self._access_token

        try:
            response: AuthResponse = await self._http_client.request(bearer_token=self._refresh_token,
                                                                     endpoint=self._endpoint_base,
                                                                     method="POST",
                                                                     data=None)
        except HttpError as e:
            if e.status_code == 400:
                raise BadAuthRequestError(e.status_code,f"Malformed authentication request: refresh token is invalid or unusable: {e.status_code}") from e
            elif e.status_code == 401:
                raise InvalidCredentialsError(e.status_code,f"Invalid credentials or expired token: {e.status_code}") from e
            elif e.status_code == 422:
                raise AuthenticationError(e.status_code,f"Authentication request validation failed: {e.status_code}") from e
            else:
                raise AuthenticationError(e.status_code, f"Authentication failed [{e.status_code}]: {e.message}") from e

        self._access_token = response["access_token"]
        self._access_token_expiration = datetime.now() + timedelta(minutes=5)
        return self._access_token


    def _is_access_token_valid(self) -> bool:
        return (self._access_token is not None
                and self._access_token_expiration is not None
                and datetime.now() < self._access_token_expiration)
import pytest

from dotenv import load_dotenv
from unittest.mock import AsyncMock
from datetime import datetime, timedelta
from Offers_sdk.Core.Errors.http_errors import HttpError
from Offers_sdk.Services.Products.auth_service import AuthService
from Offers_sdk.Core.Errors.Authentication_errors.authentication_errors import (BadAuthRequestError,
                                                                               InvalidCredentialsError,
                                                                                AuthenticationError)


@pytest.mark.asyncio
class TestAuthServiceAuthenticate:
    def setup_method(self):
        load_dotenv()

        self.http_client = AsyncMock()
        self.service = AuthService(self.http_client)

    async def test_returns_cached_token(self):
        self.service._access_token = "cached_token"
        self.service._access_token_expiration = datetime.now() + timedelta(minutes=5)

        result = await self.service.authenticate()
        assert result == "cached_token"

    async def test_bad_request_error(self):
        self.http_client.request.side_effect = HttpError(status_code=400)
        with pytest.raises(BadAuthRequestError):
            await self.service.authenticate()

    async def test_invalid_credentials_error(self):
        self.http_client.request.side_effect = HttpError(status_code=401)
        with pytest.raises(InvalidCredentialsError):
            await self.service.authenticate()

    async def test_validation_error(self):
        self.http_client.request.side_effect = HttpError(status_code=422)
        with pytest.raises(AuthenticationError):
            await self.service.authenticate()

    async def test_generic_error(self):
        self.http_client.request.side_effect = HttpError(status_code=500)
        with pytest.raises(AuthenticationError):
            await self.service.authenticate()

from Offers_sdk.Core.Errors.http_errors import HttpError


class AuthenticationError(HttpError):
    def __init__(self, status_code: int, message: str, details: object = None):
        super().__init__(status_code, message, details)
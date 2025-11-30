from Offers_sdk.Core.Errors.Authentication_errors.authentication_error import AuthenticationError


class BadAuthRequestError(AuthenticationError):
    def __init__(self, status_code: int, message: str, details: object = None):
        super().__init__(status_code, message, details)

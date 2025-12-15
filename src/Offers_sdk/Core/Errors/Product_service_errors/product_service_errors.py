from src.Offers_sdk.Core.Errors.http_errors import HttpError


class ProductServiceError(HttpError):
    def __init__(self, status_code: int, message: str, details: object = None):
        super().__init__(status_code, message, details)


class IdNotFoundError(ProductServiceError):
    def __init__(self, status_code: int, message: str, details: object = None):
        super().__init__(status_code, message, details)


class ProductAlreadyExistsError(ProductServiceError):
    def __init__(self, status_code: int, message: str, details: object = None):
        super().__init__(status_code, message, details)


class UnauthorizedAccessError(ProductServiceError):
    def __init__(self, status_code: int, message: str, details: object = None):
        super().__init__(status_code, message, details)
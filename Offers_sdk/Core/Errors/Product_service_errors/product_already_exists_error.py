from Offers_sdk.Core.Errors.Product_service_errors.product_service_errors import ProductServiceError


class ProductAlreadyExistsError(ProductServiceError):
    def __init__(self, status_code: int, message: str, details: object = None):
        super().__init__(status_code, message, details)
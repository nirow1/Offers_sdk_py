class InvalidProductIdError(Exception):
    """Exception raised for invalid product ID format."""

    def __init__(self, message="The product ID format is invalid."):
        self.message = message
        super().__init__(self.message)


class InvalidProductPayloadError(Exception):
    """Exception raised for invalid product payloads in the Offers API."""

    def __init__(self, message="The product payload is invalid."):
        self.message = message
        super().__init__(self.message)


class ProductAuthenticationError(Exception):
    """Exception raised for invalid product payloads in the Offers API."""

    def __init__(self, message="The product payload is invalid."):
        self.message = message
        super().__init__(self.message)


class ProductOffersFetchError(Exception):
    """Exception raised for invalid product payloads in the Offers API."""

    def __init__(self, message="The product payload is invalid"):
        self.message = message
        super().__init__(self.message)


class ProductRegistrationError(Exception):
    """Exception raised for invalid product payloads in the Offers API."""

    def __init__(self, message="The product payload is invalid."):
        self.message = message
        super().__init__(self.message)
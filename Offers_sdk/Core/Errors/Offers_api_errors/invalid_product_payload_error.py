class InvalidProductPayloadError(Exception):
    """Exception raised for invalid product payloads in the Offers API."""

    def __init__(self, message="The product payload is invalid."):
        self.message = message
        super().__init__(self.message)
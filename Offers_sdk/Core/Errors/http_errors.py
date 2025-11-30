class HttpError(Exception):

    def __init__(self, status_code: int, message: str = "", details: object = None):
        self.message = message or self.default_message()
        self._status_code: int = status_code
        self._details: object = details
        super().__init__(self.message)

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def details(self) -> object:
        return self._details

    @staticmethod
    def default_message() -> str:
        return "An HTTP error occurred."
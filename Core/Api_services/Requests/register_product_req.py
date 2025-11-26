from typing import TypedDict


class RegisterProductRequest(TypedDict):
    id: str
    name: str
    description: str
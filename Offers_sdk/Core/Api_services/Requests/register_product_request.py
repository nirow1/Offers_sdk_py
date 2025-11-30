from typing import TypedDict
from uuid import UUID


class RegisterProductRequest(TypedDict):
    id: UUID
    name: str
    description: str
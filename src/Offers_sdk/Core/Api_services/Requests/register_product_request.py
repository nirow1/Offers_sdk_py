from pydantic.dataclasses import dataclass
from pydantic import ConfigDict
from uuid import UUID


@dataclass(config=ConfigDict(strict=True))
class RegisterProductRequest:
    id: UUID
    name: str
    description: str

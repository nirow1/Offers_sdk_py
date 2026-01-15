from dataclasses import dataclass
from uuid import UUID


@dataclass
class RegisterProductRequest:
    #todo validation in this level, also for the responses
    id: UUID
    name: str
    description: str

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }
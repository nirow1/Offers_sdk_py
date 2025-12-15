from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ProductOffersResponse:
    id: UUID
    price: int
    items_in_stock: int

    @classmethod
    def from_dict(cls, data: dict) -> "ProductOffersResponse":
        return cls(
            id=UUID(data["id"]),
            price=int(data["price"]),
            items_in_stock=int(data["items_in_stock"]),
        )
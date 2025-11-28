from uuid import UUID
from typing import TypedDict


class ProductOffersResponse(TypedDict):
    id: UUID
    price: int
    items_in_stock: int
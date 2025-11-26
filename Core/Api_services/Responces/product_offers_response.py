from typing import TypedDict


class ProductOffersResponse(TypedDict):
    id: str
    price: float
    items_in_stock: int
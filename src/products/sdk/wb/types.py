from typing import TypedDict


class WbPrice(TypedDict):
    basic: int
    product: int


class WbSize(TypedDict):
    name: str
    origName: str
    price: WbPrice


class WbProduct(TypedDict):
    name: str
    sizes: list[WbSize]
    rating: float
    feedbacks: int

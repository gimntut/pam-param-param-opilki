from decimal import Decimal
from typing import Protocol, TypeAlias, TypedDict, NotRequired


class ProductDTO(TypedDict):
    id: NotRequired[int]
    name: str
    price: Decimal
    discount_price: Decimal
    rating: Decimal
    review_count: int


ProductDtoMap: TypeAlias = dict[str, ProductDTO]


class IWbSdk(Protocol):
    def search(self, text: str) -> ProductDtoMap:
        pass

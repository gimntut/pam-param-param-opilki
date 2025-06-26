from typing import Protocol, TypeAlias, TypedDict, Mapping, NotRequired
from decimal import Decimal


class ProductDTO(TypedDict):
    id: NotRequired[int]
    name: str
    price: Decimal
    price_with_discount: Decimal
    rating: Decimal
    review_count: int


ProductDtoMap: TypeAlias = dict[str, ProductDTO]


class IWbSdk(Protocol):
    def search(self, text: str) -> ProductDtoMap:
        pass

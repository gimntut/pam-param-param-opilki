from decimal import Decimal

from products.sdk.wb.types import WbProduct
from products.services.interfaces import ProductDTO, ProductDtoMap


def get_product_dto_map(product_item: WbProduct) -> ProductDtoMap:
    name = product_item["name"]
    sub_products = product_item["sizes"]
    result = {}
    for sub_product in sub_products:
        sub_name = sub_product["name"]
        sub_origin_name = sub_product["origName"]
        if sub_name and sub_origin_name and sub_name != sub_origin_name:
            sub_name = f"{sub_name} / {sub_origin_name}"
        sub_name = f"{name} ({sub_name})" if sub_name else name
        prices = sub_product["price"]
        sub_product_item = ProductDTO(
            name=sub_name,
            price=Decimal(prices["basic"]) / 100,
            price_with_discount=Decimal(prices["product"]) / 100,
            # По-хорошему, нужно было брать rating, но reviewRating интереснее
            rating=Decimal(product_item["reviewRating"]),
            review_count=product_item["feedbacks"],
        )
        result[sub_name] = sub_product_item
    return result

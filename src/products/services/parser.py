from dataclasses import dataclass

from django.db import transaction

from products.models import Product
from products.services.events import ProductsUpdateEvent, ProductsCreateEvent
from products.services.interfaces import IWbSdk
from utils.event_bus import event_bus


@dataclass
class ProductUpdater:
    sdk: IWbSdk

    def __call__(self, search_str: str):
        product_map = self.sdk.search(search_str)
        products = Product.objects.filter(name__in=product_map.keys())
        update_products = []
        for product in products:
            sub_product = product_map.pop(product.name)
            sub_product["id"] = product.id
            update_products.append(Product(**sub_product))
        insert_products = [Product(**product) for product in product_map.values()]
        with transaction.atomic():
            update_count = Product.objects.bulk_update(
                update_products,
                fields=[
                    "name",
                    "price",
                    "price_with_discount",
                    "rating",
                    "review_count",
                ],
            )
            event_bus.push(ProductsUpdateEvent(update_count))

            insert_count = len(Product.objects.bulk_create(insert_products))
            event_bus.push(ProductsCreateEvent(insert_count))

            event_bus.publish()

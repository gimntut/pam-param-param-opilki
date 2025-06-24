from decimal import Decimal
import json
from pathlib import Path
from pprint import pformat
from django.core.management.base import BaseCommand

from products.models import Product


class Command(BaseCommand):
    help = "Парсинг wildberries"

    def add_arguments(self, parser):
        parser.add_argument("search", nargs="+")

    def handle(self, *args, **options):
        products = []
        boots_file = Path(__file__).parent / "files" / "boots.json"
        boots = json.load(boots_file.open())
        data = boots["data"]["products"]
        for item in data:
            name = item["name"]
            sub_products = item["sizes"]
            for sub_product in sub_products:
                sub_name = sub_product["name"]
                sub_origin_name = sub_product["origName"]
                if sub_name and sub_origin_name and name != sub_origin_name:
                    sub_name = f"{sub_name} / {sub_origin_name}"
                sub_name = f"{name} ({sub_name})" if sub_name else name
                if sub_name:
                    sub_name = sub_name.replace(" ", "")
                prices = sub_product["price"]
                sub_product_item = {
                    "name": sub_name,
                    "price": Decimal(prices["basic"]) / 100,
                    "price_with_discount": Decimal(prices["product"]) / 100,
                    "rate": item["reviewRating"],
                    "review_count": item["feedbacks"],
                }
                products.append(Product(**sub_product_item))
        Product.objects.bulk_create(products)

from typing import TYPE_CHECKING

from django.core.management.base import BaseCommand

from products.sdk.wb.file_sdk import FileWbSdk
from products.services.events import ProductsCreateEvent, ProductsUpdateEvent
from products.services.product_updater import ProductUpdater


class Command(BaseCommand):
    help = "Парсинг wildberries"

    def handle_create_products(self, event: ProductsCreateEvent):
        self.stdout.write(f"Создано продуктов: {event.count}")

    def handle_update_products(self, event: ProductsCreateEvent):
        self.stdout.write(f"Обновлено продуктов: {event.count}")

    def add_arguments(self, parser: "ArgumentParser"):
        parser.add_argument("search_text", type=str)

    def handle(self, *args, **options):
        create_subscribe = ProductsCreateEvent.register(self.handle_create_products)
        update_subscribe = ProductsUpdateEvent.register(self.handle_update_products)
        search_text = options["search_text"]
        wb_sdk = FileWbSdk()
        product_updater = ProductUpdater(wb_sdk)
        product_updater(search_text)
        create_subscribe.disable()
        update_subscribe.disable()


if TYPE_CHECKING:
    from argparse import ArgumentParser

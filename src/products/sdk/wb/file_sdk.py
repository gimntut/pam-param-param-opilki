import json
from dataclasses import dataclass
from pathlib import Path

from products.sdk.wb.helpers import get_product_dto_map
from products.services.interfaces import IWbSdk, ProductDtoMap


@dataclass
class FileWbSdk(IWbSdk):
    filename: str | None = None

    def search(self, text: str) -> ProductDtoMap:
        if self.filename:
            boots_file = Path(self.filename)
        else:
            boots_file = Path(__file__).parent / "files" / "boots.json"
        boots = json.load(boots_file.open())
        data = boots["data"]["products"]
        sub_product_map = {}
        for item in data:
            sub_product_map.update(get_product_dto_map(item))
        return sub_product_map

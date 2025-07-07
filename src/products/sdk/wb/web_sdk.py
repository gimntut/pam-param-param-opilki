from typing import Final

import requests

from products.sdk.wb.helpers import get_product_dto_map
from products.services.interfaces import IWbSdk, ProductDtoMap

# Лень разбираться, какие параметры за что отвечают, поэтому оставляем все, как есть
DEFAULT_PARAMS: Final = {
    "ab_testing": "false",
    "appType": "1",
    "curr": "rub",
    "dest": "-1257786",
    "hide_dtype": "13",
    "lang": "ru",
    "page": "1",
    "resultset": "catalog",
    "sort": "popular",
    "spp": "30",
    "suppressSpellcheck": "false",
}


class WebWbSdk(IWbSdk):
    def search(self, text: str) -> ProductDtoMap:
        # Обрабатывается только первая страница, т.к. это не противоречит заданию
        url = "https://search.wb.ru/exactmatch/ru/common/v13/search"
        params = DEFAULT_PARAMS | {"query": text}
        response = requests.get(url, params=params)
        response_data = response.json()
        data = response_data["data"]["products"]
        sub_product_map = {}
        for item in data:
            sub_product_map.update(get_product_dto_map(item))
        return sub_product_map

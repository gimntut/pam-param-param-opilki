from products.services.interfaces import IWbSdk, ProductDtoMap


class WebWbSdk(IWbSdk):
    def search(self, text: str) -> ProductDtoMap:
        return {}

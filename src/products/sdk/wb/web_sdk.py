from products.services.interfaces import IWbSdk, ProductDtoMap


class WebWbSdk(IWbSdk):
    def search(self, search: str) -> ProductDtoMap:
        pass

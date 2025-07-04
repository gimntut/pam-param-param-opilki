import json

from django.core.paginator import Paginator
from django.db.models import Min, Max, Count, Q
from django.utils.safestring import mark_safe
from django.views.generic import ListView

from products.api.filtersets import ProductFilterSet
from products.backends import FilterBackend
from products.models import Product
from products.types import BarSeries
from utils.types import HttpRequest

BAR_COUNT = 10


class ProductListView(ListView):
    queryset = Product.objects.all()
    paginator_class = Paginator
    paginate_by = 10
    filter_backend = FilterBackend()
    filterset_class = ProductFilterSet
    request: HttpRequest
    price_range: dict

    def get_queryset(self):
        queryset = Product.objects.order_by("name")
        queryset = self.filter_backend.filter_queryset(self.request, queryset, self)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        qs = self.object_list
        price_range = self.queryset.aggregate(
            min_available_price=Min("price"),
            max_available_price=Max("price"),
        )
        get_bar_series = None
        if all(price_range.values()):
            get_bar_series = mark_safe(
                json.dumps(self.get_bar_series(qs, **price_range))
            )
        return super().get_context_data(
            object_list=object_list,
            filter_form=self.form,
            bar_series=get_bar_series,
            **price_range,
        )

    @staticmethod
    def get_bar_series(qs, min_available_price, max_available_price) -> list[BarSeries]:
        delta = max_available_price - min_available_price
        bar_delta = delta / BAR_COUNT
        aggregates = {}
        for i in range(BAR_COUNT):
            bar_price = min_available_price + i * bar_delta
            aggregates[f"{bar_price:.0f}"] = Count(
                "id",
                filter=Q(price__gte=bar_price, price__lt=bar_price + bar_delta),
            )
        prices = qs.aggregate(**aggregates)
        data = [{"x": x, "y": y} for x, y in prices.items()]
        return [{"data": data}]

    def get_template_names(self):
        if self.request.htmx:
            return ["products/partials/product_table.html"]
        return super().get_template_names()

    @property
    def form(self):
        backend = self.filter_backend
        filterset = backend.get_filterset(self.request, self.queryset, self)
        return filterset.form

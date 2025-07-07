import json

from django.core.paginator import Paginator
from django.db.models import Min, Max, Count, Q, Avg
from django.utils.safestring import mark_safe
from django.views.generic import ListView

from products.api.filtersets import ProductFilterSet
from products.backends import FilterBackend
from products.models import Product
from products.types import BarSeries, LineSeries
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
        bar_series = line_series = None
        if all(price_range.values()):
            bar_series = mark_safe(json.dumps(self.get_bar_series(qs, **price_range)))
            line_series = mark_safe(json.dumps(self.get_line_series(qs)))
        return super().get_context_data(
            object_list=object_list,
            filter_form=self.form,
            bar_series=bar_series,
            line_series=line_series,
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

    @staticmethod
    def get_line_series(qs) -> list[LineSeries]:
        aggregates = {}
        for rating in range(1, 6):
            avg_filter = Q(rating=rating)
            aggregates[f"price_{rating}"] = Avg("price", filter=avg_filter)
            aggregates[f"discount_price_{rating}"] = Avg(
                "discount_price", filter=avg_filter
            )
        aggregated_discounts = qs.aggregate(**aggregates)
        # Не самый хороший алгоритм вычисления скидки по рейтингу,
        # но так как в задаче алгоритм не описан, то пусть будет так
        data = []
        for rating in range(1, 6):
            avg_price = aggregated_discounts[f"price_{rating}"] or 1
            avg_discount_price = aggregated_discounts[f"discount_price_{rating}"] or 0
            discount = 100 - ((avg_price - avg_discount_price) / avg_price * 100)
            data.append({"x": str(rating), "y": round(discount)})
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

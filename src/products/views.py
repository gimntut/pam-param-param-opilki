from django.core.paginator import Paginator
from django.db.models import Min, Max
from django.views.generic import ListView, TemplateView

from products.api.filtersets import ProductFilterSet
from products.backends import FilterBackend
from products.models import Product
from utils.types import HttpRequest


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
        self.price_range = queryset.aggregate(
            available_min_price=Min("price"),
            available_max_price=Max("price"),
        )
        queryset = self.filter_backend.filter_queryset(self.request, queryset, self)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(
            object_list=object_list,
            filter_form=self.form,
            **self.price_range,
        )

    def get_template_names(self):
        if self.request.htmx:
            return ["products/partials/product_table.html"]
        return super().get_template_names()

    @property
    def form(self):
        backend = self.filter_backend
        filterset = backend.get_filterset(self.request, self.queryset, self)
        return filterset.form


class ChartView(TemplateView):
    template_name = "products/chart.html"

from django.core.paginator import Paginator
from django.views.generic import ListView, TemplateView

from products.api.filtersets import ProductFilterSet
from products.backends import FilterBackend
from products.models import Product


class ProductListView(ListView):
    queryset = Product.objects.all()
    paginator_class = Paginator
    paginate_by = 10
    filter_backend = FilterBackend()
    filterset_class = ProductFilterSet

    def get_queryset(self):
        queryset = Product.objects.order_by("name")
        queryset = self.filter_backend.filter_queryset(self.request, queryset, self)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        filterset = self.filter_backend.get_filterset(self.request, self.queryset, self)
        kwargs["filter_form"] = filterset.form
        return super().get_context_data(object_list=object_list, **kwargs)


class ChartView(TemplateView):
    template_name = "products/chart.html"

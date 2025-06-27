from django.core.paginator import Paginator
from django.views.generic import ListView, TemplateView
from django_filters.rest_framework import DjangoFilterBackend

from products.api.filtersets import ProductFilterSet
from products.models import Product


class FilterBackend(DjangoFilterBackend):

    def get_filterset_kwargs(self, request, queryset, view):
        return {
            "data": request.GET,
            "queryset": queryset,
            "request": request,
        }


class ProductListView(ListView):
    filter_backend = FilterBackend()
    filterset_class = ProductFilterSet
    paginator_class = Paginator
    paginate_by = 10

    def get_queryset(self):
        queryset = Product.objects.all()
        queryset = self.filter_backend.filter_queryset(self.request, queryset, self)
        return queryset

    def render_to_response(self, context, **response_kwargs):
        print(context)
        return super().render_to_response(context, **response_kwargs)


class ChartView(TemplateView):
    template_name = "products/chart.html"

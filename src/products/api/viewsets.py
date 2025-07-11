from rest_framework import viewsets, permissions, pagination
from rest_framework.mixins import ListModelMixin

from . import serializers, filtersets
from ..models import Product


# Create your views here.
class ProductViewSet(ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    filterset_class = filtersets.ProductFilterSet
    pagination_class = pagination.PageNumberPagination

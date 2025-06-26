from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.mixins import ListModelMixin

from . import serializers, filtersets
from ..models import Product


# Create your views here.
class ProductViewSet(ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Product.objects.all()
    filter_backends = (DjangoFilterBackend,)
    serializer_class = serializers.ProductSerializer
    filterset_class = filtersets.ProductFilterSet

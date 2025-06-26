from django.urls import path, include
from rest_framework.routers import SimpleRouter

from products.api import viewsets

router = SimpleRouter()
router.register("products", viewsets.ProductViewSet, basename="product")
urlpatterns = [
    path("", include(router.urls)),
]

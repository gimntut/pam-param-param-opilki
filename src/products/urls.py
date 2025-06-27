from django.urls import path

from products.views import ProductListView, ChartView

urlpatterns = [
    path("", ProductListView.as_view(), name="index"),
    path("chart", ChartView.as_view(), name="chart"),
]

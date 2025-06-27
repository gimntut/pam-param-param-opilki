from django_filters import FilterSet, NumberFilter


class ProductFilterSet(FilterSet):
    min_price = NumberFilter("discount_price", "gte")
    max_price = NumberFilter("discount_price", "lte")
    min_rating = NumberFilter("rating", "gte")
    max_rating = NumberFilter("rating", "lte")
    min_review_count = NumberFilter("review_count", "gte")
    max_review_count = NumberFilter("review_count", "lte")

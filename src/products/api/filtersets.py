from django_filters import FilterSet, NumberFilter, ChoiceFilter

RATING_CHOICES = (
    (1, "⭐"),
    (2, "⭐⭐"),
    (3, "⭐⭐⭐"),
    (4, "⭐⭐⭐⭐"),
    (5, "⭐⭐⭐⭐⭐"),
)


class ProductFilterSet(FilterSet):
    min_price = NumberFilter("price", "gte")
    max_price = NumberFilter("price", "lte")
    min_rating = ChoiceFilter("rating", "gte", choices=RATING_CHOICES)
    max_rating = ChoiceFilter("rating", "lte", choices=RATING_CHOICES)
    min_review_count = NumberFilter("review_count", "gte")
    max_review_count = NumberFilter("review_count", "lte")

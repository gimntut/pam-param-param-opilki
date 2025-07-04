from django_filters.rest_framework import DjangoFilterBackend


class FilterBackend(DjangoFilterBackend):
    def get_filterset_kwargs(self, request, queryset, view):
        return {
            "data": request.GET,
            "queryset": queryset,
            "request": request,
        }

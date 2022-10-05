from django_filters import filterset
from core import models


class StateFilter(filterset.FilterSet):
    name = filterset.CharFilter(lookup_expr='unaccent__icontains')
    abbreviation = filterset.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.State
        fields = ['name', 'abbreviation']

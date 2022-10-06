from django.db.models import Q
from django_filters import filterset
from core import models


class StateFilter(filterset.FilterSet):
    # name = filterset.CharFilter(lookup_expr='unaccent__icontains')
    # abbreviation = filterset.CharFilter(lookup_expr='icontains')
    name_or_abbreviation = filterset.CharFilter(method='filter_name_or_abbreviation')

    def filter_name_or_abbreviation(self, queryset, name, value):
        return queryset.filter(Q(name__unaccent__icontains=value) | Q(abbreviation__unaccent__icontains=value))

    class Meta:
        model = models.State
        fields = ['name_or_abbreviation']


class EmployeeFilter(filterset.FilterSet):
    # start_salary = filterset.NumberFilter(field_name='salary', lookup_expr='gte')
    # end_salary = filterset.NumberFilter(field_name='salary', lookup_expr='lte')
    salary = filterset.BaseRangeFilter(lookup_expr='range')
    salary_in = filterset.BaseInFilter(field_name='salary', lookup_expr='in')

    class Meta:
        model = models.Employee
        fields = ['salary', 'salary_in']


class SaleItemFilter(filterset.FilterSet):
    sale = filterset.NumberFilter(lookup_expr='exact')

    class Meta:
        model = models.SaleItem
        fields = ['sale']

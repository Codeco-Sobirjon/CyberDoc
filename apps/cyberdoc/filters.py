import django_filters

from apps.cyberdoc.models import OrderWork


class OrderWorkFilter(django_filters.FilterSet):
    number_of_order = django_filters.CharFilter(lookup_expr='icontains', label='Number of Order')
    deadline = django_filters.DateFilter(lookup_expr='lte', label='Deadline')

    class Meta:
        model = OrderWork
        fields = ['number_of_order', 'deadline']

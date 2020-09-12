from django_filters import rest_framework as filters

from .models import Order


class OrederDateFilter(filters.FilterSet):
    class Meta:
        model = Order
        fields = {'order_created_datetime': ['day', 'day__gt', 'day__lt', 'year', 'year__gt', 'year__lt', 'month',
                                             'month__gt', 'month__lt']}

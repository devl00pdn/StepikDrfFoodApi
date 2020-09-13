from django_filters import rest_framework as filters

from .models import Order


class OrederDateFilter(filters.FilterSet):
    class Meta:
        model = Order
        fields = {'published': ['date']}

from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer

from .models import Recipient, ProductSets, Order


class RecipientSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Recipient
        fields = [
            'id',
            'url',
            'surname',
            'name',
            'patronymic',
            'phone_number',
            'delivery_address'
        ]


class ProductSetsSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = ProductSets
        fields = [
            'id',
            'url',
            'title',
            'description'
        ]


class OrderSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'url',
            'order_created_datetime',
            'delivery_datetime',
            'recipient',
            'product_set',
            'status'
        ]

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import Order, ProductSets, Recipient
from .serializers import OrderSerializer, ProductSetsSerializer, RecipientSerializer


class OrdersViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def destroy(self, request, pk=None, *args, **kwargs):
        order = get_object_or_404(self.queryset, pk=pk)
        order.status = Order.STATUS_CANCELLED
        order.save()
        return Response(status=status.HTTP_200_OK)


class ProductSetsViewSet(ReadOnlyModelViewSet):
    queryset = ProductSets.objects.all()
    serializer_class = ProductSetsSerializer


class RecipientViewSet(ModelViewSet):
    queryset = Recipient.objects.all()
    serializer_class = RecipientSerializer

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import Order, ProductSets, Recipient
from .serializers import OrderSerializer, ProductSetsSerializer, RecipientSerializer


class OrdersViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # permission_classes = [AllowAny]


class ProductSetsViewSet(ReadOnlyModelViewSet):
    queryset = ProductSets.objects.all()
    serializer_class = ProductSetsSerializer
    # permission_classes = [AllowAny]


class RecipientViewSet(ModelViewSet):
    queryset = Recipient.objects.all()
    serializer_class = RecipientSerializer
    # permission_classes = [AllowAny]

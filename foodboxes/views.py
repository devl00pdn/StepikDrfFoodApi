from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import OrederDateFilter
from .models import Order, ProductSets, Recipient
from .serializers import OrderSerializer, ProductSetsSerializer, RecipientSerializer, RecipientNameSerializer, \
    RecipientDeliveryAddressSerializer


class OrdersViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    # Для фильтрации заказов по дате создания: /orders/?published__date=YYYY-MM-DD
    filterset_class = OrederDateFilter

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
    # эти поля запрещены для обновления через detail endpoint
    __forbid_update_fields = ['name', 'surname', 'patronymic', 'delivery_address']

    @action(methods=['patch'], detail=True)
    def change_name(self, request, pk=None):
        serializer = RecipientNameSerializer(self.get_object(), data=request.data, partial=True,
                                             context={'request': request})
        if serializer.is_valid():
            self.perform_update(serializer)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)

    @action(methods=['patch'], detail=True)
    def change_delivery_address(self, request, pk=None):
        serializer = RecipientDeliveryAddressSerializer(self.get_object(), data=request.data,
                                                        context={'request': request})
        if serializer.is_valid():
            self.perform_update(serializer)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        if self.__is_there_forbid_fields(request):
            return Response({'error': 'request has forbided for update fields'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = RecipientSerializer(self.get_object(), data=request.data, partial=True,
                                         context={'request': request})
        if serializer.is_valid():
            self.perform_update(serializer)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        if self.__is_there_forbid_fields(request):
            return Response({'error': 'request has forbided for update fields'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = RecipientSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            self.perform_update(serializer)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)

    def __is_there_forbid_fields(self, request):
        for field in request.data.keys():
            if field in self.__forbid_update_fields:
                return True
        return False

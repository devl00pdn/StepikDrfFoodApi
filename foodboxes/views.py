
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from proxy.content import ContentSource, ContentSourceException


@api_view(http_method_names=['GET'])
def recipients_handler(request, pk=None):
    result = None
    try:
        recipients = ContentSource().request_recipients()
    except ContentSourceException as ex:
        return Response(status=ex.status)
    if not pk:
        result = [{
            'surname': p['info']['surname'],
            'name': p['info']['name'],
            'patronymic': p['info']['patronymic'],
            'phoneNumber': p['contacts']['phoneNumber']
        } for p in recipients]
    else:
        for person in recipients:
            if person['id'] == pk:
                result = {
                    'surname': person['info']['surname'],
                    'name': person['info']['name'],
                    'patronymic': person['info']['patronymic'],
                    'phoneNumber': person['contacts']['phoneNumber']
                }
    if not result:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(result)


@api_view(http_method_names=['GET'])
def specific_product_handler(request, pk):
    try:
        foodboxes = ContentSource().request_foodboxes()
    except ContentSourceException as ex:
        return Response(status=ex.status)
    for fb in foodboxes:
        if fb['inner_id'] == pk:
            result = {
                'title': fb['name'],
                'description': fb['about'],
                'price': fb['price'],
                'weight': fb['weight_grams']
            }
            return Response(result)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(http_method_names=['GET'])
def all_products_handler(request):
    try:
        foodboxes = ContentSource().request_foodboxes()
    except ContentSourceException as ex:
        return Response(status=ex.status)
    result = [{
        'title': fb['name'],
        'description': fb['about'],
        'price': fb['price'],
        'weight': fb['weight_grams']
    } for fb in foodboxes]
    if request.query_params:
        min_weight = int(request.query_params.get('min_weight')) if request.query_params.get('min_weight') else None
        min_price = int(request.query_params.get('min_price')) if request.query_params.get('min_price') else None
        if min_weight:
            result = [item for item in result if item['weight'] >= min_weight]
        if min_price:
            result = [item for item in result if item['price'] >= min_price]
    return Response(result)

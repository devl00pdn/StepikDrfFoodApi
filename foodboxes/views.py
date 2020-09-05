import requests
from requests import ConnectionError, Timeout
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


class ContentSourceException(BaseException):
    def __init__(self, error: status):
        self.status = error


class ContentSource:
    __foodboxes_source = 'https://stepik.org/media/attachments/course/73594/foodboxes.json'
    __recipients_source = 'https://stepik.org/media/attachments/course/73594/recipients.json'

    def request_foodboxes(self):
        """
        emmit ContentSourceException
        :return: list of foodboxes
        """
        return self.__request_dataset(self.__foodboxes_source)

    def request_recipients(self):
        """
        emmit ContentSourceException
        :return: list of recipients
        """
        return self.__request_dataset(self.__recipients_source)

    def __request_dataset(self, url: str):
        result = None
        try:
            resp = requests.get(url, timeout=3)
            if resp.status_code == 200:
                result = resp.json()
        except ConnectionError:
            raise ContentSourceException(status.HTTP_404_NOT_FOUND)
        except Timeout:
            raise ContentSourceException(status.HTTP_408_REQUEST_TIMEOUT)
        if not result:
            raise ContentSourceException(status.HTTP_404_NOT_FOUND)
        return result


@api_view(http_method_names=['GET'])
def recipients_handler(request, id=None):
    result = None
    try:
        recipients = ContentSource().request_recipients()
    except ContentSourceException as ex:
        return Response(status=ex.status)
    if not id:
        result = [{
            'surname': p['info']['surname'],
            'name': p['info']['name'],
            'patronymic': p['info']['patronymic'],
            'phoneNumber': p['contacts']['phoneNumber']
        } for p in recipients]
    else:
        for person in recipients:
            if person['id'] == id:
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
def specific_product_handler(request, id):
    try:
        foodboxes = ContentSource().request_foodboxes()
    except ContentSourceException as ex:
        return Response(status=ex.status)
    for fb in foodboxes:
        if fb['inner_id'] == id:
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
            result = [item for item in result if item['weight'] < min_weight]
        if min_price:
            result = [item for item in result if item['price'] < min_price]
    return Response(result)

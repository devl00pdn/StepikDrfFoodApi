import requests
from requests import ConnectionError, Timeout
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


class ContentSource:
    class Exceptions(BaseException):
        def __init__(self, error: status):
            self.status = error

    __foodboxes_source = 'https://stepik.org/media/attachments/course/73594/foodboxes.json'
    __recipients_source = 'https://stepik.org/media/attachments/course/73594/recipients.json'

    def request_foodboxes(self):
        """
        emmit Exceptions()
        :return: list of foodboxes
        """
        return self.__request_dataset(self.__foodboxes_source)

    def request_recipients(self):
        """
        emmit Exceptions()
        :return: list of recipients
        """
        return self.__request_dataset(self.__recipients_source)

    def __request_dataset(self, url: str):
        result = None
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                result = resp.json()
        except ConnectionError:
            raise ContentSource().Exceptions(status.HTTP_404_NOT_FOUND)
        except Timeout:
            raise ContentSource().Exceptions(status.HTTP_408_REQUEST_TIMEOUT)
        if not result:
            raise ContentSource().Exceptions(status.HTTP_404_NOT_FOUND)
        return result


@api_view(http_method_names=['GET'])
def recipients_handler(request, id=None):
    result = None
    cs = ContentSource()
    try:
        recipients = cs.request_recipients()
    except ContentSource().Exceptions as ex:
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
def product_set_handler(request, id=None):
    result = None
    cs = ContentSource()
    try:
        foodboxes = cs.request_foodboxes()
    except ContentSource().Exceptions as ex:
        return Response(status=ex.status)

    # обработка фильтров
    if request.query_params:
        # фильтр минимальной цены
        min_price = request.query_params.get('min_price')
        if min_price:
            result = [{
                'title': fb['name'],
                'description': fb['about'],
                'price': fb['price'],
                'weight': fb['weight_grams']
            } for fb in foodboxes if fb['price'] < int(min_price)]
            return Response(result)
        # фильтр минимальго веса
        min_weight = request.query_params.get('min_weight')
        if min_weight:
            result = [{
                'title': fb['name'],
                'description': fb['about'],
                'price': fb['price'],
                'weight': fb['weight_grams']
            } for fb in foodboxes if fb['weight_grams'] < int(min_weight)]
            return Response(result)
    if not id:
        # Запрос всего списка наборов
        result = [{
            'title': fb['name'],
            'description': fb['about'],
            'price': fb['price'],
            'weight': fb['weight_grams']
        } for fb in foodboxes]
        return Response(result)
    else:
        # Запрос конкретного набора
        for fb in foodboxes:
            if fb['inner_id'] == id:
                result = {
                    'title': fb['name'],
                    'description': fb['about'],
                    'price': fb['price'],
                    'weight': fb['weight_grams']
                }
                return Response(result)
    # ни один из кейсов не сработал
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(http_method_names=['GET'])
def product_set_min_price_handler(request):
    result = []
    if request.query_params:
        min_price = request.query_params.get('min_price')
        if min_price:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    cs = ContentSource()
    try:
        foodboxes = cs.request_foodboxes()
    except ContentSource().Exceptions as ex:
        return Response(status=ex.status)
    result = [{
        'title': fb['name'],
        'description': fb['about'],
        'price': fb['price'],
        'weight': fb['weight_grams']
    } for fb in foodboxes if fb['price'] < min_price]
    return Response(result)


@api_view(http_method_names=['GET'])
def product_set_min_weight_handler(request):
    result = []
    if request.query_params:
        min_weight = request.query_params.get('min_weight')
        if not min_weight:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    cs = ContentSource()
    try:
        foodboxes = cs.request_foodboxes()
    except ContentSource().Exceptions as ex:
        return Response(status=ex.status)
    result = [{
        'title': fb['name'],
        'description': fb['about'],
        'price': fb['price'],
        'weight': fb['weight_grams']
    } for fb in foodboxes if fb['weight_grams'] < min_weight]
    return Response(result)

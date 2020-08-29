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

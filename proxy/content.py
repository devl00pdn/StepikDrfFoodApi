import requests
from requests import ConnectionError, Timeout
from rest_framework import status


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

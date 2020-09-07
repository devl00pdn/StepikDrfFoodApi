from django.core.management.base import BaseCommand

from foodboxes.models import ProductSets
from proxy.content import ContentSource, ContentSourceException


class Command(BaseCommand):
    help = 'delete all objects from DB and reinitialize it by default values'

    def handle(self, *args, **kwargs):
        try:
            products = ContentSource().request_foodboxes()
        except ContentSourceException as ex:
            print('Ошибка при получении данных с сервера Stepik')
            print(ex.status)
            return

        ProductSets.objects.all().delete()

        # fill database
        [ProductSets.objects.create(title=product['name'], description=product['about']) for product in products if
         'name' in product and 'about' in product]

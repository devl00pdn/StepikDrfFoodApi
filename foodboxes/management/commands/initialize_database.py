from datetime import datetime, timedelta
from random import randint

from django.core.management.base import BaseCommand
from django.utils import timezone
from foodboxes.models import ProductSets, Recipient, Order
from proxy.content import ContentSource, ContentSourceException


class Command(BaseCommand):
    help = 'delete all objects from DB and reinitialize it by default values'

    def handle(self, *args, **kwargs):
        try:
            products = ContentSource().request_foodboxes()
            recipients = ContentSource().request_recipients()
        except ContentSourceException as ex:
            print('Ошибка при получении данных с сервера Stepik')
            print(ex.status)
            return

        ProductSets.objects.all().delete()
        Recipient.objects.all().delete()
        Order.objects.all().delete()

        # fill database
        [ProductSets.objects.create(title=product['name'], description=product['about']) for product in products if
         'name' in product and 'about' in product]
        for recipient in recipients:
            Recipient.objects.create(surname=recipient['info']['surname'], name=recipient['info']['name'],
                                     patronymic=recipient['info']['patronymic'],
                                     phone_number=recipient['contacts']['phoneNumber'],
                                     delivery_address=recipient['address'])

        # create some orders
        # BUG
        for recipient in Recipient.objects.all():
            Order.objects.create(delivery_datetime=timezone.now() + timedelta(hours=1),
                                 recipient=recipient,
                                 product_set=ProductSets.objects.all()[randint(0, len(ProductSets.objects.all()) - 1)])


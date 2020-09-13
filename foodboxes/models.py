from django.db import models


class ProductSets(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)


class Recipient(models.Model):
    surname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    delivery_address = models.CharField(max_length=200)


class Order(models.Model):
    STATUS_CREATED = 'CREATED'
    STATUS_DELIVERED = 'DELIVERED'
    STATUS_PROCESSED = 'PROCESSED'
    STATUS_CANCELLED = 'CANCELLED'
    STATUS_CHOICES = [
        (STATUS_CREATED, 'Created'),
        (STATUS_DELIVERED, 'Delivered'),
        (STATUS_PROCESSED, 'Processed'),
        (STATUS_CANCELLED, 'Cancelled')
    ]
    published = models.DateTimeField(auto_now=True)
    delivery_datetime = models.DateTimeField()
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE, related_name='orders')
    product_set = models.ForeignKey(ProductSets, on_delete=models.SET_NULL, related_name='orders', null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_CREATED)

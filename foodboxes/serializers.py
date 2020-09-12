from datetime import datetime

from rest_framework.fields import DateTimeField
from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework.validators import UniqueTogetherValidator, ValidationError

from .models import Recipient, ProductSets, Order


class RecipientSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Recipient
        validators = [
            UniqueTogetherValidator(
                queryset=Recipient.objects.all(),
                fields=['surname', 'name', 'patronymic']
            )
        ]
        fields = [
            'id',
            'url',
            'surname',
            'name',
            'patronymic',
            'phone_number',
            'delivery_address'
        ]

    def validate(self, attrs):
        # Валидируем ФИО
        fields = ['surname', 'name', 'patronymic']
        # Достаём поля из запроса
        name_parts = {part: attrs[part] for part in fields if part in attrs}
        # Подсатавляем недостающие поля из обьекта модели
        recipient = self.instance
        name_parts.update({part: getattr(recipient, part) for part in fields if part not in name_parts.keys()})
        if len(name_parts) > 1:
            name_parts_pairs = list(name_parts.items())
            for index in range(len(name_parts)):
                if name_parts_pairs[index][1] == name_parts_pairs[index - 1][1]:
                    raise ValidationError(
                        detail=f'{name_parts_pairs[index][0]} and {name_parts_pairs[index - 1][0]} mast be different',
                        code=400,
                    )
        return attrs

    def validate_phone_number(self, number):
        import phonenumbers
        from phonenumbers.phonenumberutil import NumberParseException
        adapted_number = number
        # ловим код 8 в начале номера, так как он не парсится phonenumbers
        if adapted_number[0] == '8':
            adapted_number = '+7' + adapted_number[1:]
        try:
            phone = phonenumbers.parse(adapted_number)
        except NumberParseException as ex:
            raise ValidationError(
                detail=str(ex),
                code=400
            )
        if not phonenumbers.is_possible_number(phone):
            raise ValidationError(
                detail='phone number is not possible for this region',
                code=400
            )
        return number


class ProductSetsSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = ProductSets
        fields = [
            'id',
            'url',
            'title',
            'description'
        ]


class OrderSerializer(HyperlinkedModelSerializer):
    delivery_datetime = DateTimeField(input_formats=["%d-%m-%Y %H:%M"])

    class Meta:
        model = Order
        fields = [
            'id',
            'url',
            'order_created_datetime',
            'delivery_datetime',
            'recipient',
            'product_set',
            'status'
        ]

    def validate_delivery_datetime(self, delivery_datetime: datetime):
        # Время доставки не может быть меньше настоящего времени
        dt = delivery_datetime - datetime.now(tz=delivery_datetime.tzinfo)
        if dt.days < 0:
            raise ValidationError(
                detail='delivery date and time cannot be less than actual time',
                code=400
            )
        return delivery_datetime

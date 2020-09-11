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
        name_parts = {part: attrs[part] for part in fields if part in attrs}
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

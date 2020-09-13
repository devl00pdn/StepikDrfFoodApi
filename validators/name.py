from rest_framework.validators import ValidationError


def validate_name(attrs, instance):
    fields = ['surname', 'name', 'patronymic']
    # Достаём поля из запроса
    name_parts = {part: attrs[part] for part in fields if part in attrs}
    # Подсатавляем недостающие поля из обьекта модели
    recipient = instance
    name_parts.update({part: getattr(recipient, part) for part in fields if part not in name_parts.keys()})
    if len(name_parts) > 1:
        name_parts_pairs = list(name_parts.items())
        for index in range(len(name_parts)):
            if name_parts_pairs[index][1] == name_parts_pairs[index - 1][1]:
                raise ValidationError(
                    detail=f'{name_parts_pairs[index][0]} and {name_parts_pairs[index - 1][0]} mast be different',
                    code=400,
                )

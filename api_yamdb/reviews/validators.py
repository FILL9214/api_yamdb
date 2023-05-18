from django.core.exceptions import ValidationError


def validate_username(name):
    if name == 'me':
        raise ValidationError(
            'Имя пользователя "me" использовать запрещено!',
            params={'name': name},
        )

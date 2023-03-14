from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

INVALID_USER_NAME = ['me', ]

validate_symbols = RegexValidator(
    r'^[0-9a-zA-Zа-яА-Я\w.@+-]*$',
    'Допустимы только прописные или строчные буквы, '
    'а так же символы: @ . + - _'
)


def validate_user_name(value):
    if value.lower() in INVALID_USER_NAME:
        raise ValidationError(
            _('"%(value)s" - недопустимое имя пользователя,'
              ' пожалуйста, выберете другое'),
            params={'value': value},
        )


def not_self_subscribe(user, author):
    if user == author:
        raise serializers.ValidationError(
            'Вы не можете подписываться на самого себя.'
        )

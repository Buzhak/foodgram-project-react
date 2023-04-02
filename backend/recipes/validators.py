import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

HEX = '^#[0-9A-F]{6}$'


def hex_color_validaror(value):
    if re.match(HEX, value) is None:
        raise ValidationError(
            _('%(value)s укажите цвет в "HEX" формате - "#******"'),
            params={'value': value},
        )


def positive_number_validator(value):
    if value < 0:
        raise ValidationError(
            _('Пожалуйста укажите значение числом больше нуля.'),
            params={'value': value},
        )

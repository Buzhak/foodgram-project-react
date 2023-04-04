import random
import string

from django.conf import settings
from django.core.mail import send_mail as django_send_mail

from .constants import TOKEN_LENGHT

my_email = settings.YAMDB_EMAIL


def get_code() -> str:
    '''
    Функция генерирует строку символов длиной "length" символов.
    '''

    char_set = string.ascii_letters + string.digits
    return ''.join(random.sample(char_set, TOKEN_LENGHT))


def send_email(email: str, confirmation_code: str, username: str):
    '''
    Функция отправления email.
    '''
    django_send_mail(
        'Ваш код',
        f'username: {username}, "confirmation_code": {confirmation_code}',
        my_email,
        [email],  # Это поле "Кому" (можно указать список адресов)
        fail_silently=False,  # Сообщать об ошибках («молчать ли об ошибках?»)
    )

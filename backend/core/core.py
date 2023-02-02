import random
import string

from django.conf import settings
from django.core.mail import send_mail as django_send_mail
from rest_framework_simplejwt.tokens import AccessToken

my_email = settings.YAMDB_EMAIL


def get_code(length: int) -> str:
    '''
    Функция генерирует строку символов длиной "length" символов.
    '''
    char_set = string.ascii_letters + string.digits
    return ''.join(random.sample(char_set, length))


def delete_tokens_for_user():
    '''
    Функция отдёт токен  для пользвателя
    '''
    print('токен удалён') #нужно как-то удалить токен


def get_tokens_for_user(user):
    '''
    Функция удаляет токен пользователя
    '''
    token = AccessToken.for_user(user)
    return {'auth_token': str(token)}



def send_email(email: str, confirmation_code: str, username: str):
    django_send_mail(
        'Ваш код',
        f'username: {username}, "confirmation_code": {confirmation_code}',
        my_email,
        [email],  # Это поле "Кому" (можно указать список адресов)
        fail_silently=False,  # Сообщать об ошибках («молчать ли об ошибках?»)
    )

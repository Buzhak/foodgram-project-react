import random
import string

from django.conf import settings
from django.core.mail import send_mail as django_send_mail
from django.shortcuts import get_list_or_404

from recipes.models import Ingredient, ShopingCart

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


def create_shopping_list(user) -> str:
    cart = ShopingCart.objects.filter(user=user)
    shopping_list = ''
    for recipe in cart:
        shopping_list += ('_' * 30 + '\n')
        shopping_list += ('' + '\n')
        shopping_list += (f'{recipe.recipe}' + '\n')
        shopping_list += ('' + '\n')
        ingredients = get_list_or_404(Ingredient, recipe=recipe.recipe)
        count = 0
        for ingredient in ingredients:
            count += 1
            shopping_list += (f'{count}. {ingredient}' + '\n')
    shopping_list += ('_' * 30 + '\n')
    return shopping_list

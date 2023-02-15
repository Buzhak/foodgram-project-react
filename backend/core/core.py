import random
import string

from django.conf import settings
from django.core.mail import send_mail as django_send_mail
from django.shortcuts import get_list_or_404
from rest_framework_simplejwt.tokens import AccessToken
from .constants import TOKEN_LENGHT
from recipes.models import Ingredient, Shoping_cart

my_email = settings.YAMDB_EMAIL



def get_code() -> str:
    '''
    Функция генерирует строку символов длиной "length" символов.
    '''
    char_set = string.ascii_letters + string.digits
    return ''.join(random.sample(char_set, TOKEN_LENGHT))

def send_email(email: str, confirmation_code: str, username: str):
    django_send_mail(
        'Ваш код',
        f'username: {username}, "confirmation_code": {confirmation_code}',
        my_email,
        [email],  # Это поле "Кому" (можно указать список адресов)
        fail_silently=False,  # Сообщать об ошибках («молчать ли об ошибках?»)
    )

def print_recipes(user):
    cart = Shoping_cart.objects.filter(user=user)
    for recipe in cart:
        print('_' * 30)
        print('')
        print(recipe.recipe)
        print('')
        ingredients = get_list_or_404(Ingredient, recipe=recipe.recipe)
        count = 0
        for ingredient in ingredients:
            count += 1
            print(f'{count}. {ingredient}')
    print('_' * 30)

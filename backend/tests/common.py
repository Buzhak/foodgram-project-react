from rest_framework.test import APIClient

from recipes.models import Tag, Product
from users.models import User


PASSWORD = "random123"
NAME = "random"

def auth_client(username: str, email: str, is_admin=False):
    data = {
        "email": email,
        "username": username,
        "first_name": NAME,
        "last_name": NAME,
        "password": PASSWORD
    }
    # client = APIClient()
    # client.post('/api/users/', data=data)
    if is_admin:
        User.objects.create_superuser(**data)
    else:
        User.objects.create_user(**data)
    client = APIClient()
    data_login = {
        "password": PASSWORD,
        "email": email 
    }
    response = client.post('/api/auth/token/login/', data=data_login)
    data = response.json()
    token = data['auth_token']
    auth_client = APIClient()
    auth_client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    
    return auth_client


def create_tag_data():
    data = [
        {
            "name": "Завтрак",
            "color": "#E26C2D",
            "slug": "breakfast"
        },
        {
            "name": "Обед",
            "color": "#E2FF2D",
            "slug": "lunch"
        },
        {
            "name": "Ужин",
            "color": "#AAAAAA",
            "slug": "dinner"
        }
    ]
    data = [Tag(**i) for i in data]
    Tag.objects.bulk_create(
        data
    )

def create_product():
    Product.objects.create(
        name='Картошка',
        measurement_unit='шт.'
    )


def create_recipe_data(auth_client):
    create_product()
    data = {
            'ingredients': [],
            'name': 'some_name',
            'tags': [],
            'cooking_time': 1
        }
    response = auth_client.post('/api/recipes/', data, format='json')
    return response
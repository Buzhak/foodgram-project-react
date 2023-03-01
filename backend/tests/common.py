from rest_framework.test import APIClient

from recipes.models import Tag, Product


PASSWORD = "random123"

def auth_client(username: str, email: str):
    data = {
        "email": email,
        "username": username,
        "first_name": "random",
        "last_name": "random",
        "password": PASSWORD
    }
    client = APIClient()
    client.post('/api/users/', data=data)
    data_login = {
        "password": "random123",
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
        name='one',
        measurement_unit='two'
    )


def create_recipe_data(auth_client):
    create_product()
    data = {
        "ingredients": [
            {
            "id": 1,
            "amount": 10
            }
        ],
        "name": "string",
        "text": "string",
        "cooking_time": 1
    }
    auth_client.post('/api/recipes/', data = data)
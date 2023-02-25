
from rest_framework.test import APIClient


EMAIL = "random@lol.lol"
PASSWORD = "random123"

def auth_client():
    data = {
        "email": EMAIL,
        "username": "random",
        "first_name": "random",
        "last_name": "random",
        "password": PASSWORD
    }
    client = APIClient()
    client.post('/api/users/', data=data)
    data_login = {
        "password": "random123",
        "email": EMAIL 
    }
    response = client.post('/api/auth/token/login/', data=data_login)
    data = response.json()
    token = data['auth_token']
    auth_client = APIClient()
    auth_client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    
    return auth_client
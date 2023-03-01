import pytest
from rest_framework.test import APIClient

from .common import auth_client, create_product, create_tag_data
from recipes.models import Product, Tag, Recipe


class Test_recipes_api():
    list = '/api/recipes/'
    detail = '/api/recipes/1/'
    
    @pytest.mark.django_db(transaction=True)
    def test_recipe_api(self, client):

        response = client.get(self.list)

        assert response.status_code == 200, (
                f'GET метод `{self.list}` должен юбыть доступен всем пользователям'
            )
        
        response = client.post(self.list)

        assert response.status_code == 401, (
                f'POST метод `{self.list}` должен быть доступен только аутентифицированным пользователям'
            )
        
        response = client.patch(self.detail)

        assert response.status_code == 401, (
                f'PATCH метод `{self.detail}` должен быть доступен только аутентифицированным пользователям'
            )

        response = client.delete(self.detail)
        
        assert response.status_code == 401, (
                f'DELETE метод `{self.detail}` должен быть доступен только аутентифицированным пользователям'
            )

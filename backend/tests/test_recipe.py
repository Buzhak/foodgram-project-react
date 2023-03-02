import pytest
from rest_framework.test import APIClient
from django.shortcuts import get_object_or_404

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

        new_user = auth_client('user', 'user@ya.ru')
        response = new_user.get(self.list)

        assert response.status_code == 200, (
            f'GET метод `{self.list}` должен юбыть доступен всем пользователям'
        )

        data = {
            'ingredients': [],
            'name': 'some_name',
            'tags': [],
            'cooking_time': 1
        }
        response = new_user.post(self.list, data, format='json')

        assert response.status_code == 201, (
            f'POST метод `{self.list}` должен быть доступен только аутентифицированным пользователям'
        )

        response = new_user.get(self.detail)

        assert response.status_code == 200, (
            f'GET метод `{self.detail}` должен быть доступен только аутентифицированным пользователям'
        )

        data_update = {
            'ingredients': [],
            'name': 'some_name',
            'tags': [],
            'cooking_time': 100
        }
        response = new_user.patch(self.detail, data_update, format='json')

        assert response.status_code == 200, (
            f'PATCH метод `{self.detail}` должен быть доступен только аутентифицированным пользователям'
        )
        
        recipe = get_object_or_404(Recipe, id=1)

        assert recipe.cooking_time == 100, (
            f'Метод PATCH не работает. Нет изменения записи в БД'
        )

        response = new_user.delete(self.detail)
        
        assert response.status_code == 204, (
            f'DELETE метод `{self.detail}` должен быть доступен только аутентифицированным пользователям'
        )

        assert not Recipe.objects.filter(id=1).exists(), (
            'запись должна удаляться из БД после успешного DELETE метода'
        )

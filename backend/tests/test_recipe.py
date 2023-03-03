import pytest
from rest_framework.test import APIClient
from django.shortcuts import get_object_or_404

from .common import auth_client, create_product, create_tag_data, create_recipe_data
from recipes.models import Product, Tag, Recipe


class Test_recipes_api():
    list = '/api/recipes/'
    detail = '/api/recipes/1/'
    detail_2 = '/api/recipes/2/'

    
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

        user_1 = auth_client('user', 'user@ya.ru')
        user_2 = new_user = auth_client('user_2', 'user_2@ya.ru')
        admin = auth_client('admin', 'admin@ya.ru', is_admin=True)
        response = user_1.get(self.list)

        assert response.status_code == 200, (
            f'GET метод `{self.list}` должен юбыть доступен всем пользователям'
        )


        response = create_recipe_data(user_1)

        assert response.status_code == 201, (
            f'POST метод `{self.list}` должен быть доступен только аутентифицированным пользователям'
        )

        response = user_1.get(self.detail)

        assert response.status_code == 200, (
            f'GET метод `{self.detail}` должен быть доступен только аутентифицированным пользователям'
        )

        response = user_2.get(self.detail)

        assert response.status_code == 200, (
            f'GET метод `{self.detail}` должен быть доступен другим аутентифицированным пользователям'
        )

        data_update = {
            'ingredients': [],
            'name': 'some_name',
            'tags': [],
            'cooking_time': 100
        }
        response = user_1.patch(self.detail, data_update, format='json')

        assert response.status_code == 200, (
            f'PATCH метод `{self.detail}` должен быть доступен только автору рецепта'
        )

        response = user_2.patch(self.detail, data_update, format='json')

        assert response.status_code == 403, (
            f'PATCH метод `{self.detail}` НЕ должен быть доступен другим аутентифицированным пользователям'
        )
        
        recipe = get_object_or_404(Recipe, id=1)

        assert recipe.cooking_time == 100, (
            f'Метод PATCH не работает. Нет изменения записи в БД'
        )

        response = user_2.delete(self.detail)
        
        assert response.status_code == 403, (
            f'DELETE метод `{self.detail}` НЕ должен быть доступен другим аутентифицированным пользователям'
        )

        response = user_1.delete(self.detail)
        
        assert response.status_code == 204, (
            f'DELETE метод `{self.detail}` должен быть доступен только автору рецепта'
        )

        assert not Recipe.objects.filter(id=1).exists(), (
            'запись должна удаляться из БД после успешного DELETE метода'
        )

        create_recipe_data(user_1)

        response = admin.patch(self.detail_2, data_update, format='json')

        assert response.status_code == 200, (
            f'PATCH метод `{self.detail_2}` должен быть доступен админу'
        )
        
        response = admin.delete(self.detail_2)
        
        assert response.status_code == 204, (
            f'DELETE метод `{self.detail_2}` должен быть доступен админу'
        )

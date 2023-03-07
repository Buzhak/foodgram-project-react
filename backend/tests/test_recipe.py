import pytest
from rest_framework.test import APIClient
from django.shortcuts import get_object_or_404

from .common import auth_client, create_product, create_recipe_data
from recipes.models import Recipe


class Test_recipes_api():

    @pytest.mark.django_db(transaction=True)
    def test_recipe_api(self, client):
        user_1 = auth_client('user', 'user@ya.ru')
        user_2 = new_user = auth_client('user_2', 'user_2@ya.ru')
        admin = auth_client('admin', 'admin@ya.ru', is_admin=True)

        resepe_data_1 = create_recipe_data(user_1)
        resepe_data_2 = create_recipe_data(user_1)

        recipe_list = '/api/recipes/'
        detail = f'/api/recipes/{resepe_data_1.data["id"]}/'
        detail_2 = f'/api/recipes/{resepe_data_2.data["id"]}/'


        assert resepe_data_1.status_code == 201, (
            f'POST метод `{recipe_list}` должен быть доступен только аутентифицированным пользователям'
        )
        response = user_1.get(recipe_list)

        assert response.status_code == 200, (
            f'GET метод `{recipe_list}` должен юбыть доступен всем пользователям'
        )

        response = user_1.get(detail)
        res = Recipe.objects.all()
        assert response.status_code == 200, (
            f'GET метод `{detail}`должен быть доступен только аутентифицированным пользователям'
        )

        response = user_2.get(detail)

        assert response.status_code == 200, (
            f'GET метод `{detail}` должен быть доступен другим аутентифицированным пользователям'
        )

        data_update = {
            'ingredients': [],
            'name': 'some_name',
            'tags': [],
            'cooking_time': 100
        }
        response = user_1.patch(detail, data_update, format='json')

        assert response.status_code == 200, (
            f'PATCH метод `{detail}` должен быть доступен только автору рецепта'
        )

        response = user_2.patch(detail, data_update, format='json')

        assert response.status_code == 403, (
            f'PATCH метод `{detail}` НЕ должен быть доступен другим аутентифицированным пользователям'
        )
        
        recipe = get_object_or_404(Recipe, id=2)

        assert recipe.cooking_time == 100, (
            f'Метод PATCH не работает. Нет изменения записи в БД'
        )

        response = user_2.delete(detail)
        
        assert response.status_code == 403, (
            f'DELETE метод `{detail}` НЕ должен быть доступен другим аутентифицированным пользователям'
        )

        response = user_1.delete(detail)
        
        assert response.status_code == 204, (
            f'DELETE метод `{detail}` должен быть доступен только автору рецепта'
        )

        assert not Recipe.objects.filter(id=1).exists(), (
            'запись должна удаляться из БД после успешного DELETE метода'
        )

        response = admin.patch(detail_2, data_update, format='json')

        assert response.status_code == 200, (
            f'PATCH метод `{detail_2}` должен быть доступен админу'
        )
        
        response = admin.delete(detail_2)
        
        assert response.status_code == 204, (
            f'DELETE метод `{detail_2}` должен быть доступен админу'
        )

        response = client.get(recipe_list)

        assert response.status_code == 200, (
            f'GET метод `{recipe_list}` должен юбыть доступен всем пользователям'
        )
        
        response = client.post(recipe_list)

        assert response.status_code == 401, (
            f'POST метод `{recipe_list}` должен быть доступен только аутентифицированным пользователям'
        )
        
        response = client.patch(detail)
        
        assert response.status_code == 401, (
            f'PATCH метод `{detail}` должен быть доступен только аутентифицированным пользователям'
        )

        response = client.delete(detail)
        
        assert response.status_code == 401, (
            f'DELETE метод `{detail}` должен быть доступен только аутентифицированным пользователям'
        )

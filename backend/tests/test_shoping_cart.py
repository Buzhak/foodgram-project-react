import pytest

from .common import auth_client, create_product, create_recipe_data

from recipes.models import Recipe


class Test_shoping_cart_api():
    

    @pytest.mark.django_db(transaction=True)
    def test_shoping_cart_api(self, client):

        user_1 = auth_client('some_user', 'some@email.com')
        recipe_data = create_recipe_data(user_1)

        download = '/api/recipes/download_shopping_cart/'
        create_or_delete = f'/api/recipes/{recipe_data.data["id"]}/shopping_cart/'

        response = client.get(download)

        assert response.status_code == 401, (
            f'GET метод `{download}` не должен работать для не авторизованного пользователя'
        )

        response = client.post(create_or_delete)

        assert response.status_code == 401, (
            f'POST метод `{create_or_delete}` не должен работать для не авторизованного пользователя'
        )

        response = client.delete(create_or_delete)

        assert response.status_code == 401, (
            f'DELETE метод `{create_or_delete}` не должен работать для не авторизованного пользователя'
        )

        response = user_1.post(create_or_delete) 

        assert response.status_code == 201, (
            f'POST метод `{create_or_delete}` должен работать для авторизованного пользователя'
        )

        response = user_1.post(create_or_delete) 

        assert response.status_code == 400, (
            f'POST метод `{create_or_delete}` не должен работать если в корзине покупок уже есть такой рецепт'
        )

        response = user_1.delete(create_or_delete) 

        assert response.status_code == 204, (
            f'DELETE метод `{create_or_delete}` не должен работать для не авторизованного пользователя'
        )
        
        response = user_1.get(download)

        assert response.status_code == 200, (
            f'GET метод `{download}` не должен работать для не авторизованного пользователя'
        )
         
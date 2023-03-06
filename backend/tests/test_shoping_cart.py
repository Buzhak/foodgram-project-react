import pytest

from .common import auth_client, create_product, create_recipe_data

from recipes.models import Recipe


class Test_shoping_cart_api():
    download = '/api/recipes/download_shopping_cart/'
    create_or_delete = '/api/recipes/3/shopping_cart/'

    @pytest.mark.django_db(transaction=True)
    def test_shoping_cart_api(self, client):
        response = client.get(self.download)

        assert response.status_code == 401, (
            f'GET метод `{self.download}` не должен работать для не авторизованного пользователя'
        )

        response = client.get(self.download)

        assert response.status_code == 401, (
            f'POST метод `{self.create_or_delete}` не должен работать для не авторизованного пользователя'
        )

        response = client.delete(self.download)

        assert response.status_code == 401, (
            f'DELETE метод `{self.create_or_delete}` не должен работать для не авторизованного пользователя'
        )
        
        user_1 = auth_client('some_user', 'some@email.com')
        create_recipe_data(user_1)

        response = user_1.post(self.create_or_delete) 

        assert response.status_code == 201, (
            f'POST метод `{self.create_or_delete}` должен работать для авторизованного пользователя'
        )

        response = user_1.post(self.create_or_delete) 

        assert response.status_code == 400, (
            f'POST метод `{self.create_or_delete}` не должен работать если в корзине покупок уже есть такой рецепт'
        )

        response = user_1.delete(self.create_or_delete) 

        assert response.status_code == 400, (
            f'DELETE метод `{self.create_or_delete}` не должен работать для не авторизованного пользователя'
        )
        
        response = user_1.get(self.download)

        assert response.status_code == 200, (
            f'GET метод `{self.download}` не должен работать для не авторизованного пользователя'
        )
         
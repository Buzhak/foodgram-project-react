import pytest

from .common import create_product
from recipes.models import Product


class Test_ingredients():
    

    @pytest.mark.django_db(transaction=True)
    def test_ingredients_api(self, client):
        create_product()
        product = Product.objects.all().order_by('-id')[:1] 

        product_list = '/api/ingredients/'
        search_product = '/api/ingredients/?search=к'
        product_detail = f'/api/ingredients/{product[0].id}/'

        response = client.get(product_list)

        assert response.status_code == 200, (
            f'GET метод `{product_list}` должен быть доступен для всех пользователей'
        )

        response = client.get(search_product)

        assert response.status_code == 200, (
            f'GET метод `{search_product}` должен быть доступен для всех пользователей'
        )

        response = client.get(product_detail)

        assert response.status_code == 200, (
            f'GET метод `{product_detail}` должен быть доступен для всех пользователей'
        )
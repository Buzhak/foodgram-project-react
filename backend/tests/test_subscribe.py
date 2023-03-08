import pytest

from django.shortcuts import get_object_or_404

from .common import auth_client
from users.models import User

class Test_subscribes():
    
    @pytest.mark.django_db(transaction=True)
    def test_subscribes(self, client):
        user_1_client = auth_client('user_1', 'user_1@some.com')
        user_2_client = auth_client('user_2', 'user_2@some.com')

        user_1 = get_object_or_404(User, username = 'user_1')
        user_2 = get_object_or_404(User, username = 'user_2')

        my_subscribes = '/api/users/subscriptions/'
        add_or_delete_subscribe = f'/api/users/{user_2.id}/subscribe/'
        self_subscribe = f'/api/users/{user_1.id}/subscribe/'

        response = client.get(my_subscribes)

        assert response.status_code == 401, (
            f'GET метод `{my_subscribes}` не должен работать для не авторизованного пользователя'
        )

        response = client.post(add_or_delete_subscribe)

        assert response.status_code == 401, (
            f'POST метод `{add_or_delete_subscribe}` не должен работать для не авторизованного пользователя'
        )

        response = client.delete(add_or_delete_subscribe)

        assert response.status_code == 401, (
            f'DELETE метод `{add_or_delete_subscribe}` не должен работать для не авторизованного пользователя'
        )

        response = user_1_client.get(my_subscribes)

        assert response.status_code == 200, (
            f'GET метод `{my_subscribes}` должен работать для авторизованного пользователя'
        )

        response = user_1_client.post(add_or_delete_subscribe)

        assert response.status_code == 201, (
            f'POST метод `{add_or_delete_subscribe}` должен работать для авторизованного пользователя'
        )

        response = user_1_client.post(add_or_delete_subscribe)

        assert response.status_code == 400, (
            f'POST метод `{add_or_delete_subscribe}` авторизованный пользователь не может несколько раз подписатьна на одного и тогоже автора'
        )

        response = user_1_client.post(self_subscribe)

        assert response.status_code == 400, (
            f'POST метод `{self_subscribe}` нельзя подписываться на самого себя'
        )

        response = user_1_client.delete(add_or_delete_subscribe)

        assert response.status_code == 204, (
            f'DELETE метод `{add_or_delete_subscribe}` должен работать для авторизованного пользователя'
        )

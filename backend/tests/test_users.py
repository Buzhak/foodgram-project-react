import pytest
from rest_framework.test import APIClient

from .common import auth_client as new_client
PASSWORD = "Qwerty123"
EMAIL = "vpupkin@yandex.ru"
USERNAME = "vasya.pupkin"

class TestUserRegistration:
    user_list = '/api/users/'
    user_detil = '/api/users/2/'
    user_me = '/api/users/me/'
    set_password = '/api/users/set_password/'
    login = '/api/auth/token/login/'
    logout = '/api/auth/token/logout/'

    data_register = {
        "email": EMAIL,
        "username": USERNAME,
        "first_name": "Вася",
        "last_name": "Пупкин",
        "password": PASSWORD
    }
    wrong_data_register = {
        "first_name": "1",
        "last_name": "1",
        "password": "fgdzfdsgds"
    }
    data_set_pass = {
        "username": USERNAME,
        "password": PASSWORD
    }
    data_login = {
        "password": PASSWORD,
        "email": EMAIL 
    }
    reset_pass_data = {
        "new_password": "some_new_pass",
        "current_password": PASSWORD
    }
    wrong_token = 'sklgndsfljgds;kjgdlskjsad;kjas'

    @pytest.mark.django_db(transaction=True)
    def test_guest_users(self, client):
        response = client.get(self.user_list)

        assert response.status_code == 200, (
            'Страница при GET запросе `{self.user_list}` должна быть доступна не авторизованному пользователю'
        )
    
        response = client.post(self.user_list, data=self.data_register)

        assert response.status_code == 201, (
            'Проверьте, что при POST запросе (регистрации нового пользователя) `{self.user_list}` с правильными данными возвращает статус 201'
        )

        response = client.post(self.user_list, data=self.wrong_data_register)

        assert response.status_code == 400, (
            'Проверьте, что при POST запросе (регистрации нового пользователя) `{self.user_list}` с НЕ правильными данными возвращает статус 400'
        )

        response = client.get(self.user_detil)

        assert response.status_code == 401, (
                'Страница конкретного пользователья не должна быть доступна для не авторизованного пользователя'
            )

        response = client.get(self.user_me)
        assert response.status_code == 401, (
                'Страница текущего пользователя не должна быть доступна для не авторизованного пользователя'
            )
        
        response = client.post(self.set_password, data=self.data_set_pass)

        assert response.status_code == 401, (
                'Страница смены пароля не должна быть доступна для не авторизованного пользователя'
            )
    
        response = client.post(self.login, data=self.data_login)
        assert response.status_code != 201, (
                'Страница должна быть доступна не авторизованному пользователю'
            )

        response = client.post(self.logout)
        assert response.status_code == 401, (
                'Страница НЕ должна быть доступна не авторизованному пользователю'
            )


    @pytest.mark.django_db(transaction=True)
    def test_login_users(self, client):
        response = client.post(self.user_list, data=self.data_register)
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе (регистрации нового пользователя) `{self.user_list}` с правильными данными возвращает статус 201'
        )

        response = client.post(self.login, data=self.data_login)
        assert response.status_code != 201, (
                'Страница должна быть доступна не авторизованному пользователю'
            )

        data = response.json()
        assert 'auth_token' in data, (
                'Убедитесь, что при передаче верных данных возвращается auth_token'
            )

        token = data['auth_token']
        auth_client = APIClient()
        auth_client.credentials(HTTP_AUTHORIZATION=f'Token {token}') 
        response = auth_client.get(self.user_detil)

        assert response.status_code != 401, (
                f'Страница {self.user_detil} конкретного пользователья должны быть доступна для авторизованного пользователя'
            )
        
        response = auth_client.get(self.user_me)
        assert response.status_code == 200, (
                f'Страница {self.user_me} текущего пользователья должны быть доступна для авторизованного пользователя'
            )
        
        response = auth_client.post(self.set_password, data=self.reset_pass_data)
        assert response.status_code == 204, (
                f'Страница {self.set_password} должна быть доступна для авторизованного пользователя'
            )

        response = auth_client.post(self.logout)
        assert response.status_code == 204, (
                f'Страница {self.logout} должна быть доступна для авторизованного пользователя'
            )
  
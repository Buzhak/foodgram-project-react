import pytest

from users.models import User


class TestUserRegistration:
    user_list = '/api/users/'
    user_detil = '/api/users/1/'
    user_me = '/api/users/me/'
    set_password = '/api/users/set_password/'
    login = '/api/auth/token/login/'
    logout = '/api/auth/token/logout/'

    data_register = {
        "email": "vpupkin@yandex.ru",
        "username": "vasya.pupkin",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "password": "Qwerty123"
    }
    wrong_data_register = {
        "first_name": "1",
        "last_name": "1",
        "password": "fgdzfdsgds"
    }
    data_set_pass = {
        "username": "vasya.pupkin",
        "password": "Qwerty123"
    }
    data_login = {
        "password": "Qwerty123",
        "email": "vpupkin@yandex.ru"
        
    }

    @pytest.mark.django_db(transaction=True)
    def test_guest_get_list_users(self, client):
        response = client.get(self.user_list)

        assert response.status_code == 200, (
            'Страница при GET запросе `{self.user_list}` должна быть доступна не авторизованному пользователю'
        )


    @pytest.mark.django_db(transaction=True)
    def test_guest_create_user(self, client):
        
        response = client.post(self.user_list, data=self.data_register)

        assert response.status_code == 201, (
            'Проверьте, что при POST запросе (регистрации нового пользователя) `{self.user_list}` с правильными данными возвращает статус 201'
        )

        response = client.post(self.user_list, data=self.wrong_data_register)

        assert response.status_code == 400, (
            'Проверьте, что при POST запросе (регистрации нового пользователя) `{self.user_list}` с НЕ правильными данными возвращает статус 400'
        )

    @pytest.mark.django_db(transaction=True)
    def test_guest_get_user_detail(self, client):
        response = client.get(self.user_detil)

        assert response.status_code == 401, (
                'Страница конкретного пользователья не должна быть доступна для не авторизованного пользователя'
            )
    
    @pytest.mark.django_db(transaction=True)
    def test_guest_set_password(self, client):
        response = client.post(self.set_password, data=self.data_set_pass)

        assert response.status_code == 401, (
                'Страница смены пароля не должна быть доступна для не авторизованного пользователя'
            )
    
    @pytest.mark.django_db(transaction=True)
    def test_guest_login(self, client):
        client.post(self.user_list, data=self.data_register)
        response = client.post(self.login, data=self.data_login)
        assert response.status_code != 201, (
                'Страница должна быть доступна не авторизованному пользователю'
            )

    @pytest.mark.django_db(transaction=True)
    def test_guest_logout(self, client):
        response = client.post(self.logout)
        assert response.status_code == 401, (
                'Страница НЕ должна быть доступна не авторизованному пользователю'
            )
        
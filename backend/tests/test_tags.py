import pytest
from rest_framework.test import APIClient

from .common import create_tag_data


pytestmark = pytest.mark.django_db

class Test_tags_api():
    tags = '/api/tags/'
    tag = '/api/tags/1/'

    @pytest.mark.django_db(transaction=True)
    def test_tags_api(self, client):
        create_tag_data()
        response = client.get(self.tags)

        assert response.status_code == 200, (
                f'Страница при GET запросе `{self.tags}` должна быть доступна'
            )
        
        response = client.get(self.tag)

        assert response.status_code == 200, (
                f'Страница при GET запросе `{self.tag}` должна быть доступна'
            )

        data = response.json()

        assert 'name' in data, (
                'Поле name должно присутсвовать'
            )
        
        assert 'color' in data, (
                'Поле color должно присутсвовать'
            )
        
        assert 'slug' in data, (
                'Поле slug должно присутсвовать'
            )

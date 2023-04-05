import pathlib
from csv import DictReader

from django.conf import settings
from django.core.management import BaseCommand
from recipes.models import Product

DATA_PATH = pathlib.Path('/static/data/ingredients.csv')
SCV = {
    Product: 'ingredients.csv',
}


class Command(BaseCommand):
    '''Загрузка тестовых данных из csv в БД.'''
    def handle(self, *args, **kwargs):
        for model, file in SCV.items():
            with open(f'{settings.BASE_DIR}{DATA_PATH}',
                      'r', encoding='utf-8') as csv_file:
                reader = DictReader(csv_file)
                model.objects.bulk_create(model(**data) for data in reader)
        self.stdout.write(self.style.SUCCESS('Successfully load data'))

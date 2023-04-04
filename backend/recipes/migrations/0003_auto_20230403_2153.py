# Generated by Django 2.2.16 on 2023-04-03 21:53

from django.db import migrations, models
import recipes.validators


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20230402_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='amount',
            field=models.IntegerField(default=1, validators=[recipes.validators.positive_number_validator], verbose_name='количество'),
            preserve_default=False,
        ),
    ]
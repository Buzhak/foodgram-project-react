# Generated by Django 2.2.16 on 2023-03-20 18:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0009_auto_20230313_2231'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopingCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopingcarts', to='recipes.Recipe', verbose_name='рецепты')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopingcarts', to=settings.AUTH_USER_MODEL, verbose_name='пользователи')),
            ],
            options={
                'verbose_name': 'В корзине',
                'verbose_name_plural': 'В корзине',
            },
        ),
        migrations.DeleteModel(
            name='Shoping_cart',
        ),
        migrations.AddConstraint(
            model_name='shopingcart',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique favorite'),
        ),
    ]

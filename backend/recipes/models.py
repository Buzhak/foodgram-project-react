from django.db import models
from users.models import User


class Tag(models.Model):
    title = models.CharField('тег', max_length=256)
    color = models.CharField('цвет', max_length=7)
    slug = models.SlugField(unique=True)


class Product(models.Model):
    name = models.CharField('название продукта', max_length=200)
    measurement_unit = models.CharField('единица измерения', max_length=200)


class Ingredient(models.Model):
    INGREDIENT_DISPLAY = ( 
        'id: {id}, ' 
        'name: {product.name}, ' 
        'measurement_unit: {product.measurement_unit}, '
        'amount: {amount}'
    ) 
    product = models.ManyToManyField(
        Product,
        related_name='%(class)ss',
        verbose_name='Продукты')
    amount = models.IntegerField('количество', blank=True, null=True)


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        related_name='%(class)ss',
        verbose_name='Теги')
    author = models.ForeignKey(User,
        on_delete=models.CASCADE,
        related_name='%(class)ss',
        verbose_name='Автор')
    ingredients = models.ForeignKey()
    is_favorited = models.BooleanField(defaulf=False)
    is_in_shopping_cart = models.BooleanField(defaulf=False)
    name = models.CharField('название категории', max_length=256)
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    text = models.TextField('описание', null=True, blank=True)
    cooking_time = models.IntegerField('время приготовления в минутах')


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепты'
    )


class IngredientProduct(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name='Продукты'
    )
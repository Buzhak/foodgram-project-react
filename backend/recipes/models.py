from django.db import models
from users.models import User
from .validators import hex_color_validaror


class Tag(models.Model):
    name = models.CharField('тег', max_length=256)
    color = models.CharField('цвет', max_length=7, validators=[hex_color_validaror])
    slug = models.SlugField('слаг',unique=True)

    def __str__(self) -> str:
        return self.name

        
    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

class Product(models.Model):
    name = models.CharField('название продукта', max_length=200)
    measurement_unit = models.CharField('единица измерения', max_length=200)

    def __str__(self) -> str:
        return f'{self.name}, {self.measurement_unit}'
    
    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        related_name='%(class)ss',
        verbose_name='Теги'
        )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)ss',
        verbose_name='Автор'
        )
    name = models.CharField('название рецепта', max_length=256)
    image = models.ImageField('изображение',upload_to='resipes/images/', null=True, blank=True)
    text = models.TextField('описание',null=True, blank=True)
    cooking_time = models.IntegerField('время приготовления в минутах')
    pub_date = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return f'Рецепт: {self.name}'


class Ingredient(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='%(class)ss',
        verbose_name='Продукты')
    amount = models.IntegerField('количество', blank=True, null=True)
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='%(class)ss',
        verbose_name='Ингредиенты'
        )

    def __str__(self) -> str:
        if self.amount == 0 or self.amount is None:
            return f'{self.product.name} - по вкусу'
        return f'{self.product.name} - {self.amount} {self.product.measurement_unit}'


    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='Теги')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепты'
    )


class FavoriteAndCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)ss',
        verbose_name = 'пользователи'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='%(class)ss',
        verbose_name = 'рецепты'
    )

    class Meta:
        abstract = True


class Favorite(FavoriteAndCart):
    class Meta:
        verbose_name = 'В избранном'
        verbose_name_plural = 'В избранном'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name="unique favorite"),
        ]

    def __str__(self):
        return f'Рецепты в избранном пользователя {self.user}'


class Shoping_cart(FavoriteAndCart):
    class Meta:
        verbose_name = 'В корзине'
        verbose_name_plural = 'В корзине'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name="unique favorite"),
        ]

    def __str__(self):
        return f'Рецепты в корзине {self.user}'

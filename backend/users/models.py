from django.contrib.auth.models import AbstractUser
from django.db import models

from core.constants import CODE_LENGTH

from .validators import validate_symbols, validate_user_name


class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=254)
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[validate_user_name, validate_symbols]
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    password = models.CharField(max_length=150)

    def __str__(self):
        return self.username


class Code(models.Model):
    code = models.CharField(max_length=CODE_LENGTH)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)ss'
    )

    def __str__(self):
        return self.code


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'),
                name="unique followers"),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='Вы не можете подписаться на самого себя'),
        ]

    def __str__(self):
        return f'Подписки пользователя {self.user}'

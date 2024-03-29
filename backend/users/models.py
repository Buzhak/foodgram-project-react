from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_symbols, validate_user_name


class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=254)
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[validate_user_name, validate_symbols]
    )
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    password = models.CharField(max_length=150)

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


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

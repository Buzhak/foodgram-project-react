from core.constants import CODE_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_symbols, validate_user_name

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'
ROLES = (
    (USER, 'user'),
    (MODERATOR, 'moderator'),
    (ADMIN, 'admin')
)


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[validate_user_name, validate_symbols]
    )
    email = models.EmailField(unique=True, max_length=256)
    password = models.CharField(max_length=150, blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=200, default=USER, choices=ROLES)

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

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

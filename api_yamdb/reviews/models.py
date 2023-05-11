from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    email = models.EmailField(
        'e-mail адрес',
        max_length=100,
        unique=True,
        blank=False,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )

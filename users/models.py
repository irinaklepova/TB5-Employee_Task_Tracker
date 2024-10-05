from django.contrib.auth.models import AbstractUser
from config.settings import NULLABLE
from django.db import models


class User(AbstractUser):
    """Модель пользователя"""

    username = None
    email = models.EmailField(unique=True, verbose_name="Почта")
    phone = models.CharField(max_length=20, **NULLABLE, verbose_name="Номер телефона")
    city = models.CharField(max_length=100, **NULLABLE, verbose_name="Город")
    avatar = models.ImageField(upload_to="users/", **NULLABLE, verbose_name="Аватар")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

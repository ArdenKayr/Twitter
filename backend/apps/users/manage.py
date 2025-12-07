from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Кастомная модель пользователя.
    Наследуемся от AbstractUser, чтобы сохранить стандартную логику Django (пароли, логин),
    но добавить свои поля.
    """
    bio = models.TextField(max_length=500, blank=True, verbose_name="Биография")
    # Ссылка "сам на себя" для реализации подписок
    following = models.ManyToManyField(
        'self', 
        symmetrical=False, 
        related_name='followers', 
        blank=True
    )

    def __str__(self):
        return self.username
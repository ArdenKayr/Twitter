from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Добавляем новые поля
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    # Поля подписок у нас уже были, оставляем их
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

    def __str__(self):
        return self.username
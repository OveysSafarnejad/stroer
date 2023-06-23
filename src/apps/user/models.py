from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['email'])
        ]

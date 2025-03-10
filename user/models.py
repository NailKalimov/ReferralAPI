from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    referrer = models.ForeignKey('User',
                                 verbose_name="Реферер",
                                 blank=True,
                                 null=True,
                                 on_delete=models.SET_NULL)

    def __str__(self):
        return self.username

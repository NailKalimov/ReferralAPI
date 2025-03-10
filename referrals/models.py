from datetime import timedelta
from django.db import models

from user.models import User


class Referral(models.Model):
    code = models.CharField(verbose_name="Реферальный код", max_length=100, unique=True, blank=False)
    create_date = models.DateField(verbose_name="Дата создания", auto_created=True, auto_now=True)
    valid_period = models.IntegerField(verbose_name="Срок действия")
    end_date = models.DateField(verbose_name="Дата окончания")
    owner = models.OneToOneField(User, verbose_name="Владелец", on_delete=models.CASCADE, related_name='referral_code')

    @staticmethod
    def get_end_date(now, delta):
        return now + timedelta(days=delta)

    def __str__(self):
        return self.code

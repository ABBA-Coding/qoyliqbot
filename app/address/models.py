from ckeditor.fields import RichTextField
from django.db import models

from app.users.models import TelegramUser


class Address(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name="address")
    longitude = models.FloatField()
    latitude = models.FloatField()

    class Meta:
        verbose_name = "Manzil"
        verbose_name_plural = "Manzillar"

    def __str__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=255)
    description = RichTextField(max_length=1023, null=True, blank=True)
    longitude = models.FloatField()
    latitude = models.FloatField()
    tg_id = models.CharField(verbose_name="Telegram gruppa ID", max_length=20, null=True, blank=True)
    is_active = models.BooleanField(verbose_name="Faolmi?", default=False)

    class Meta:
        verbose_name = "Filial"
        verbose_name_plural = "Filiallar"

    def __str__(self):
        return self.name

from datetime import datetime

from django.db import models

from app.address.models import Branch
from app.users.models import TelegramUser
from django.utils.translation import gettext_lazy as _
from imagekit.models.fields import ImageSpecField, ProcessedImageField


def upload_path(instance, filename):
    today = datetime.now()
    return '{0}/{1}/{2}/{3}'.format(
        today.year,
        today.strftime('%m'),
        today.strftime('%d'),
        filename
    )


class Category(models.Model):
    name = models.CharField(verbose_name="Nomi", max_length=100)
    image = ProcessedImageField(verbose_name="Rasmi", upload_to=upload_path,
                                format='JPEG',
                                options={'quality': 60}, null=True, blank=True)
    is_active = models.BooleanField(verbose_name="Активный?", default=False)

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(verbose_name="Nomi", max_length=150)
    price = models.IntegerField(verbose_name="Narxi")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    image = ProcessedImageField(verbose_name="Rasmi", upload_to=upload_path,
                                format='JPEG',
                                options={'quality': 60}, null=True, blank=True)
    is_active = models.BooleanField(verbose_name="Активный?", default=False)

    class Meta:
        verbose_name = "Maxsulot"
        verbose_name_plural = "Maxsulotlar"

    def __str__(self):
        return self.name


class SelectedProduct(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='selected_products')
    name = models.CharField(max_length=100)
    count = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.count})"


class Order(models.Model):
    class STATUS(models.TextChoices):
        CREATED = ("created", _("Yaratildi"))
        PROCEED = ("proceed", _("Ko'rib chiqildi"))
        PAID = ("paid", _("To'landi"))

    class CashTYPE(models.TextChoices):
        CLICK = ("click", _("Click"))
        PAYME = ("payme", _("Payme"))

    comment = models.TextField(blank=True, null=True)
    cash_type = models.CharField(max_length=10, choices=CashTYPE.choices, default=CashTYPE.PAYME)
    delivery = models.CharField(max_length=3)
    address = models.CharField(max_length=500, null=True, blank=True)
    filial = models.ForeignKey(Branch, on_delete=models.CASCADE)
    distance = models.CharField(max_length=10, null=True, blank=True)
    cost = models.CharField(max_length=10, default=0)
    delivery_cost = models.CharField(max_length=10, default=0)
    all_cost = models.CharField(max_length=10)
    user = models.ForeignKey(TelegramUser, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS.choices, default=STATUS.CREATED)
    charge_id = models.CharField(max_length=50, null=True, blank=True)

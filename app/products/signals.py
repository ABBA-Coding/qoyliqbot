from aiogram.types import LabeledPrice
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync

from app.products.models import Order
from bot.misc import bot

CLICK = settings.CLICK
PAYME = settings.PAYME
CLICK_PHOTO = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTgWGCXrpS2g54YYm0eTzAHHFzY7Kj3ZXEcbg&usqp=CAU"
PAYME_PHOTO = "https://synthesis.uz/wp-content/uploads/2022/01/payme-1920x1080-1.jpg"


@receiver(post_save, sender=Order)
def send_new_user_notification(sender, instance, created, **kwargs):
    if created:
        sync_send_invoice = async_to_sync(bot.send_invoice)
        sync_send_message = async_to_sync(bot.send_message)
        price = LabeledPrice(label=str(_("Savatchangizdagi to'lov miqdori")),
                             amount=int(instance.all_cost.replace(" ", "")) * 100)
        # Prepare invoice data
        invoice_data = {
            "chat_id": instance.user_id,
            "photo_url": CLICK_PHOTO if instance.cash_type == Order.CashTYPE.CLICK else PAYME_PHOTO,
            "currency": "uzs",
            "title": "Anjan",
            "description": "Muzqaymoqlar haridi",
            "payload": str(instance.pk),
            "provider_token": CLICK if instance.cash_type == Order.CashTYPE.CLICK else PAYME,
            "prices": [price]
        }
        # Prepare message data
        message_data = {
            "chat_id": instance.user_id,
            "text": str(_("Xaridni to'lash uchun quyidagi tugma orqali to'lang"))
        }
        selected_products_message = "\n".join(
            [f"{product.name}: {product.count}" for product in instance.selected_products.all()])
        message_data["text"] += f"\n\n{selected_products_message}"
        sync_send_message(**message_data)
        sync_send_invoice(**invoice_data)

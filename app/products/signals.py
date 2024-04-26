from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync

from app.products.models import Order, SelectedProduct
from bot.misc import bot
from bot.utils.kbs import approve


@receiver(post_save, sender=Order)
def send_new_user_notification(sender, instance, created, **kwargs):
    if created:
        sync_send_message = async_to_sync(bot.send_message)
        # Prepare message data
        message_data = {
            "chat_id": instance.user_id,
            "text": str(_("Xaridingiz hodimlarga yuborildi"))
        }
        selected_products_message = "\n".join(
            [f"{product.name}: {product.count}" for product in instance.selected_products.all()])
        message_data["text"] += f"\n\n{selected_products_message}"
        sync_send_message(**message_data)
        selected_products = SelectedProduct.objects.filter(order=instance) # noqa
        products_text = "\n".join([f"{product.name}: {product.count}" for product in selected_products])

        success_text = str(_("<b>Yangi buyurtma</b>\n"
                             "Yetkazib berish: {delivery}\n"
                             "Manzil: {address}\n"
                             "Filial: {filial}\n"
                             "Masofa: {distance}\n"
                             # "Narx: {cost}\n"
                             # "Yetkazib berish narxi: {delivery_cost}\n"
                             "Jami: {all_cost}\n"
                             "Foydalanuvchi: {user}\n"
                             "Mahsulotlar:\n{products}\n"
                             "Check ID: {charge_id}\n"
                             )).format(
            delivery=str(_("Xa")) if instance.delivery == 'yes' else str(_("Yo'q")),
            address=instance.address,
            filial=instance.filial.name,  # Assuming Branch model has a 'name' field
            distance=instance.distance,
            # cost=order.cost,
            # delivery_cost=order.delivery_cost,
            all_cost=instance.all_cost,
            user=instance.user.phone if instance.user else None,  # Assuming TelegramUser has a 'username' field
            charge_id=instance.charge_id,
            products=products_text,  # Add the list of selected products to the message
        )
        sync_send_message(instance.user_id, success_text)
        sync_send_message(settings.TELEGRAM_GROUP_ID, success_text, reply_markup=approve(instance.pk))

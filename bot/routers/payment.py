from aiogram import Router, types, F
from aiogram.types import PreCheckoutQuery
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from app.products.models import Order, SelectedProduct
from app.users.models import TelegramUser as User
from bot.utils.kbs import approve

router = Router()


@router.message(F.successful_payment)
async def echo_successfull_payment(message: types.Message, user: User) -> None:
    try:
        order = await Order.objects.select_related(
            'user', 'filial').aget(pk=int(message.successful_payment.invoice_payload))
        order.status = order.STATUS.PAID
        order.charge_id = message.successful_payment.provider_payment_charge_id
        await order.asave()

        # Get the list of selected products for the order
        selected_products = SelectedProduct.objects.filter(order=order)
        products_text = "\n".join([f"{product.name}: {product.count}" async for product in selected_products])

        success_text = str(_("<b>Yangi buyurtma</b>\n"
                             "To'lov turi: {cash_type}\n"
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
            cash_type=order.get_cash_type_display(),
            delivery=str(_("Xa")) if order.delivery == 'yes' else str(_("Yo'q")),
            address=order.address,
            filial=order.filial.name,  # Assuming Branch model has a 'name' field
            distance=order.distance,
            # cost=order.cost,
            # delivery_cost=order.delivery_cost,
            all_cost=order.all_cost,
            user=order.user.phone if order.user else None,  # Assuming TelegramUser has a 'username' field
            charge_id=order.charge_id,
            products=products_text,  # Add the list of selected products to the message
        )
        await message.bot.send_message(order.user_id, success_text)
        await message.bot.send_message(settings.TELEGRAM_GROUP_ID, success_text, reply_markup=approve(order.pk))
    except Order.DoesNotExist:
        ...


@router.pre_checkout_query()
async def echo_checkout(query: PreCheckoutQuery):
    """
    id='8187792719859100214' from_user=User(id=6201336345, is_bot=False, first_name='Gayrat', last_name='Sultonov',
    username=None, language_code='ru', is_premium=None, added_to_attachment_menu=None,
    can_join_groups=None, can_read_all_group_messages=None, supports_inline_queries=None)
    currency='UZS' total_amount=10000 invoice_payload='tttt' shipping_option_id=None order_info=None
    """
    try:
        order = await Order.objects.aget(pk=int(query.invoice_payload))
        if order.status == order.STATUS.CREATED:
            await query.bot.answer_pre_checkout_query(query.id, ok=True)
            return
        error_message = str(_("Savat allaqachon to'langan"))
    except Order.DoesNotExist:
        error_message = str(_("Savat topilmadi"))
    await query.bot.answer_pre_checkout_query(query.id, ok=False, error_message=error_message)

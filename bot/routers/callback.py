from datetime import datetime
from aiogram import Router, types, F

from app.products.models import Order

router = Router()


@router.callback_query(F.data.startswith('order_'))
async def send_random_value(callback: types.CallbackQuery):
    _callback, order_id = callback.data.split("order_")
    current_time = datetime.now()
    formatted_time = current_time.strftime("%H:%M %d-%m-%Y")
    user_mention = callback.from_user.mention_html()
    edited_text = callback.message.text + "\nQabul qildi: " + user_mention + "\nKo'rilgan vaqt: " + formatted_time
    await callback.message.edit_text(edited_text, reply_markup=None)
    order = await Order.objects.aget(pk=order_id)
    order.status = order.STATUS.PROCEED
    await order.asave()

from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from django.conf import settings
from django.utils.translation import gettext_lazy as _, activate

from app.address.models import Address, Branch
from app.products.models import Order
from app.users.models import TelegramUser as User
from bot.functions import get_location_name_async
from bot.utils.kbs import menu_keyboards_dict, menu_kb, approve

router = Router()


@router.message()
async def echo_handler(message: types.Message, user: User) -> None:
    text = str(_("Bo'limni tanlang"))
    menu_text_list = [menu for emoji_list in menu_keyboards_dict.values() for menu in emoji_list]
    activate(user.language)

    if message.text and message.text in menu_text_list:
        if message.text in ("🍟 Заказать", "🍟 Buyurtma berish"):
            url = settings.HOST + "/tg/?lang=" + user.language
            await message.answer(
                str(_("Buyurtma berish uchun quyidagi tugmani bosing")),
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text=message.text,
                                web_app=WebAppInfo(url=url)
                            )
                        ]
                    ]
                ),
            )
        elif message.text in ("🏠 Filiallar", "🏠 Филиалы"):
            counter = 1
            branches = Branch.objects.filter(is_active=True)
            branches_text = str(_("🏡 Filiallar\n\n"))
            async for filial in branches:
                branches_text += str(counter) + ". " + filial.name + "\n"
                counter += 1
            await message.answer(branches_text)
        elif message.text in ("🏡 Manzillarim", "🏡 Мои адреса"):
            counter = 1
            addresses = Address.objects.filter(user=user)
            address_text = str(_("🏡 Manzillarim\n\n"))
            async for address in addresses:
                address_text += str(counter) + ". " + address.name + "\n"
                counter += 1
            await message.answer(address_text)
    elif message.location:
        name = await get_location_name_async(message.location.latitude, message.location.longitude)
        await Address.objects.aupdate_or_create(
            user=user, name=name, defaults={"longitude": message.location.longitude,
                                            "latitude": message.location.latitude}
        )
        await message.answer(text, reply_markup=menu_kb(user.language))
    else:
        await message.answer(text, reply_markup=menu_kb(user.language))

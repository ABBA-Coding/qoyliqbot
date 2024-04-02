from aiogram.utils.keyboard import ReplyKeyboardBuilder
from django.utils.translation import gettext_lazy as _
from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

languages = (
    str(_("🇺🇿 O'zbek tili")),
    str(_("🇷🇺 Русский язык"))
)
menu_keyboards_dict = {
    "ru": ("🍟 Заказать", "🏠 Филиалы", "🏡 Мои адреса"),
    "uz": ("🍟 Buyurtma berish", "🏠 Filiallar", "🏡 Manzillarim")
}
send_location_text = {
    'ru': "Отправить локацию",
    "uz": "Lokatsiya yuborish"
}


def contact_kb():
    markup = ReplyKeyboardBuilder()
    markup.add(KeyboardButton(text=str(_("Raqam yuborish")), request_contact=True))
    return markup.adjust(2).as_markup(resize_keyboard=True)


def location_kb(language='uz'):
    markup = ReplyKeyboardBuilder()
    markup.add(KeyboardButton(text=send_location_text[language], request_location=True))
    return markup.adjust(2).as_markup(resize_keyboard=True)


def language_kb():
    markup = ReplyKeyboardBuilder()
    markup.add(
        *(KeyboardButton(text=lang) for lang in languages)
    )
    return markup.adjust(2).as_markup(resize_keyboard=True)


def menu_kb(language_code='uz'):
    markup = ReplyKeyboardBuilder()
    markup.add(
        *(KeyboardButton(text=menu) for menu in menu_keyboards_dict[language_code])
    )
    markup.add(
        KeyboardButton(text=send_location_text[language_code], request_location=True)
    )
    return markup.adjust(2).as_markup(resize_keyboard=True)


def approve(order_id):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Ko'rildi",
        callback_data="order_" + str(order_id))
    )
    return builder.as_markup()

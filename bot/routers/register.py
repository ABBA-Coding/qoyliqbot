import phonenumbers
from aiogram import Router, types
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from django.utils.translation import gettext_lazy as _, activate
from aiogram.types import KeyboardButton, ReplyKeyboardRemove

from app.address.models import Address
from bot.filters.states import Registration
from app.users.models import TelegramUser as User
from bot.helpers import format_phone_number
from bot.utils.kbs import contact_kb, language_kb, languages, menu_kb, location_kb
from bot.functions import get_location_name_async

router = Router()


@router.message(Command("start"))
async def on_start(message: types.Message, state: FSMContext, user: User):
    if not user.language or not user.phone or not user.fullname:
        hello_text = ("Salom, Anjan botga xush kelibsiz!\nTilni tanlang!\n\n"
                      "Привет, добро пожаловать в Anjan bot!\nВыберите язык!")
        await message.answer(hello_text, reply_markup=language_kb())
        await state.set_state(Registration.language)
    else:
        await message.answer(str(_("Bo'limni tanlang")), reply_markup=menu_kb(user.language))


@router.message(Registration.language)
async def registration_language(message: types.Message, state: FSMContext, user: User):
    if message.text and message.text in languages:
        lang = 'uz' if message.text == languages[0] else 'ru'
        user.language = lang
        activate(lang)
        await user.asave()
        await state.set_state(Registration.fio)
        await message.answer(str(_("Iltimos, ism sharifingizni yozing")),
                             reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(str(_("Noto'g'ri buyruq")))


@router.message(Registration.fio)
async def registration_phone(message: types.Message, state: FSMContext, user: User):
    user.fullname = message.text
    await user.asave()
    markup = ReplyKeyboardBuilder()
    markup.add(KeyboardButton(text=str(_("Raqamni yuborish")), request_contact=True))  # Отправить телефон
    await message.answer(str(_("O'zingizni telefon raqamingizni yuboring")),
                         reply_markup=contact_kb())
    await state.set_state(Registration.phone)


@router.message(Registration.phone)
async def registration_phone(message: types.Message, state: FSMContext, user: User):
    error_text = str(_("Telefon raqam noto'g'ri ko'rsatildi\n"
                       "Iltimos, telefon raqamni ko'rsatilgan formatda yozing: +998 хх ххх хх хх"))
    if message.contact:
        user.phone = message.contact.phone_number
        await user.asave()
    elif message.text:
        formatted_phone = format_phone_number(message.text)
        if len(formatted_phone) == 13:
            parsed_number = phonenumbers.parse(formatted_phone)
            is_valid = phonenumbers.is_valid_number(parsed_number)
            if is_valid:
                user.phone = formatted_phone
                await user.asave()
            else:
                await message.answer(error_text, reply_markup=contact_kb())
                return
        else:
            await message.answer(error_text, reply_markup=contact_kb())
            return
    else:
        await message.answer(error_text, reply_markup=contact_kb())
        return
    await message.answer(
        str(_("Lokasiyangizni yuboring")),
        reply_markup=location_kb(user.language))
    await state.set_state(Registration.location)


@router.message(Registration.location)
async def registration_finish(message: types.Message, state: FSMContext, user: User):
    if message.location:
        name = await get_location_name_async(message.location.latitude, message.location.longitude)
        await Address.objects.acreate(user=user, name=name,
                                      longitude=message.location.longitude, latitude=message.location.latitude)
        await state.clear()
        await message.answer(
            str(_("Ro'yxatdan o'tdingiz")),
            reply_markup=menu_kb(user.language))
    else:
        await message.answer(str(_("Iltimos pastdagi tugmadan bizga o'z lokasiyangizni yuboring")))

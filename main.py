from aiogram import types, Bot, Router, Dispatcher
import asyncio
from aiogram.filters import Command
import logging
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram import F
from db import create_user,info_users
import re

PHONE_PATTERN = r"\+998[0-9]{9}"

logging.basicConfig(level=logging.INFO)
bot = Bot('6708582288:AAEdp760zuW1Hhikv8ooOG7mTMhmBcVE-kU')

form_router = Router()
dp = Dispatcher()

def inline_button():
    buttons = InlineKeyboardBuilder()
    ha = InlineKeyboardButton(text="ha", callback_data="ha")
    yoq = InlineKeyboardButton(text="yoq", callback_data="yoq")
    buttons.add(ha, yoq)
    return buttons.as_markup()

class IshJoyiKerak(StatesGroup):
    ism = State()
    yosh = State()
    texnologiya = State()
    telefon_raqam = State()
    hudud = State()
    # narh = State()
    # kasb = State()
    # vaqt = State()
    # maqsad = State()




def start_buttons() -> ReplyKeyboardMarkup:
    button_1 = KeyboardButton(text='Sherik kerka')
    button_2 = KeyboardButton(text='Ish joyi kerak')
    button_3 = KeyboardButton(text='Hodim kerak')
    button_4 = KeyboardButton(text='Ustoz kerak')
    button_5 = KeyboardButton(text='Shogirt kerak')
    button_6 = KeyboardButton(text="Foydalanuvchi ro'yxati")

    reply_buttons = ReplyKeyboardMarkup(
        keyboard=[
            [button_1, button_2],
            [button_3, button_4],
            [button_5, button_6]
        ], resize_keyboard=True
    )
    return reply_buttons

@form_router.message(Command('start'))
async def get_started(message: types.Message):
    full_name = message.from_user.full_name
    await message.answer(f'Assalomu aleykum, {full_name}', reply_markup=start_buttons())
    # await bot.send_photo(chat_id=message.chat.id, photo="https://static.vecteezy.com/vite/assets/photo-masthead-375-b8ae1548.webp", reply_markup=inline_button())


@form_router.message(F.text == "Foydalanuvchi ro'yxati")
async def info_users(message: types.Message):
    data = info_users()
    text = ""
    for user in data:
        text += f"ISM:{user[0]},TELEFON RAQAM:{user[1]}\n"

    await message.answer(text)



@form_router.message(F.text == 'Ish joyi kerak')
async def ish_joyi_kerak(message: types.Message, state: FSMContext):
    text = """Ish joyi topish uchun ariza berish
    Hozir sizga birnecha savollar beriladi. 
    Har biriga javob bering. 
    Oxirida agar hammasi togri bolsa, HA tugmasini bosing va arizangiz Adminga yuboriladi.

    Ism, familiyangizni kiriting?
    """
    await message.answer(text=text)
    await state.set_state(IshJoyiKerak.ism)
        
    
@form_router.message(IshJoyiKerak.ism)
async def set_user_name(message: types.Message, state: FSMContext):
    await state.update_data(ism=message.text)  
    text = """🕑 Yosh: 
    Yoshingizni kiriting?
    Masalan, 19
    """  
    await message.answer(text)
    await state.set_state(IshJoyiKerak.yosh)




@form_router.message(IshJoyiKerak.yosh)
async def set_user_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("Yosh faqat sonlardan iborat bo'lsin")
    await state.update_data(yosh=message.text)
    text = """📚 Texnologiya:
    Talab qilinadigan texnologiyalarni kiriting?
    Texnologiya nomlarini vergul bilan ajrating. Masalan, 

    Java, C++, C#
    """
    await message.answer(text=text)
    await state.set_state(IshJoyiKerak.texnologiya)



@form_router.message(IshJoyiKerak.texnologiya)
async def set_user_age(message: types.Message, state: FSMContext):
    await state.update_data(texnologiya=message.text)
    text = """📞 Aloqa: 
    Boglanish uchun raqamingizni kiriting?
    Masalan, +998 90 123 45 67
    """
    await message.answer(text=text)
    await state.set_state(IshJoyiKerak.telefon_raqam)



@form_router.message(IshJoyiKerak.telefon_raqam)
async def set_user_age(message: types.Message, state: FSMContext):
    if not re.match(PHONE_PATTERN, message.text):
        return await message.answer("Uzbekistan raqami bo'lishiga ishonch hosil qiling")
    await state.update_data(telefon_raqam=message.text)
    text = """🌐 Hudud: 
    Qaysi hududdansiz?
    Viloyat nomi, Toshkent shahar yoki Respublikani kiriting.
    """
    await message.answer(text=text)
    await state.set_state(IshJoyiKerak.hudud)


@form_router.message(IshJoyiKerak.hudud, F.text == "Ha" or "Yo'q")
async def send_application(message: types.Message, state: FSMContext):
    if message.text == "Yo'q":
        return await message.answer("Ma'lumotlar yuborilmadi !!!")

    data = await state.get_data()
    text = f"""👨‍💼 Xodim: {message.from_user.first_name}
    🕑 Yosh: {data['yosh']}
    📚 Texnologiya: {data['texnologiya']}
    🇺🇿 Telegram: @{message.from_user.username}
    📞 Aloqa: {data['telefon_raqam']} 
    🌐 Hudud:{data['hudud']} 
    """
    create_user(data['ism'],data['yosh'],data['texnologiya'],data['telefon_raqam'],data['hudud'])
    await state.clear()
    await bot.send_message(chat_id=1978574076, text=text)
    await message.answer("Sizning arizangiz ko'rip chiqish uchun adminga yuborildi")




@form_router.message(IshJoyiKerak.hudud)
async def set_user_age(message: types.Message, state: FSMContext):

    reply_buttons = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Ha"), KeyboardButton(text='Yo\'q')],
        ],resize_keyboard=True
    )


    await state.update_data(hudud=message.text)
    data = await state.get_data()
    print(data)
    text = f"""👨‍💼 Xodim: {message.from_user.first_name}
    🕑 Yosh: {data['yosh']}
    📚 Texnologiya: {data['texnologiya']}
    🇺🇿 Telegram: @{message.from_user.username}
    📞 Aloqa: {data['telefon_raqam']} 
    🌐 Hudud:{data['hudud']} 
    """
    await message.answer(text=text, reply_markup=reply_buttons)







async def main():
    dp.include_router(form_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
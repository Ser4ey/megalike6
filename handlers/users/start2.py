import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from loader import dp, db_of_active_users, db_of_history_users
from keyboards.default import start_menu


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    name = message.from_user.full_name
    id = message.from_user.id

    user_info = db_of_active_users.select_active_User(telegram_id=id)
    if user_info is None:
        await message.answer(f'Приветствую, {name}! Вам необходимо зарегистрироваться.\nВаш id: {id}')
        return
    await message.answer(text=f'''Приветствую, {name} 👋''', reply_markup=start_menu.start_menu_users)


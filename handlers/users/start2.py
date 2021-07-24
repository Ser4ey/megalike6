import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from loader import dp, db_of_active_users, db_of_history_users
from states import Start_new_user_reg
from keyboards.default import start_menu


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):

    name = message.from_user.full_name
    id = message.from_user.id

    await message.answer(text=f'''
Привет 👋! Это бот активности для Instagram.
С помощью этого бота вы сможете получать лайки и комментарии на свои посты.
Жми на кнопку "Расскажи правила"
    ''', reply_markup=start_menu)


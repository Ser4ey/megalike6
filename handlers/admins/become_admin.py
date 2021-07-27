import sqlite3

import data.config
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from loader import dp, db_of_active_users, db_of_history_users

from keyboards.default import start_menu


def check_admin(user_id):
    '''
    Проверяет является ли пользователь администратором
    True - da
    False - net
    '''
    admins = data.config.admins

    if str(user_id) in admins or int(user_id) in admins:
        return True
    else:
        return False


@dp.message_handler(text='admin_')
async def add_task(message: types.Message, state: FSMContext):
    '''Отпраляет админу меню админа'''
    id = message.from_user.id

    if not check_admin(id):
        # пользователь не евляется админом
        await message.answer(text=f'Вы не админ. telegram_id={id}')
        return

    await message.answer(text='Вот ваше меню, admin.', reply_markup=start_menu.start_menu_admin)




import data.config
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from loader import dp, db_of_active_users, db_of_history_users
import asyncio
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


@dp.message_handler(text='Список Участников')
async def add_task(message: types.Message, state: FSMContext):
    '''Отпраляет админу меню админа'''
    id = message.from_user.id

    if not check_admin(id):
        # пользователь не евляется админом
        await message.answer(text=f'Вы не админ. telegram_id={id}')
        return

    users = db_of_active_users.select_all_active_Users()
    for i in range(len(users)):
        text_ = f'{i+1}) {users[i]}'
        text_ = f'''
Number-{i+1}

telegram_id: {users[i][0]}
instagram_account_name: {users[i][1]}
phone_number: {users[i][2]}
registration_date: {users[i][3]}
available_links_for_today: {users[i][5]}
number_of_links_requested_today: {users[i][6]}
common_day_link_limit: {users[i][7]}
vip_status: {users[i][8]}
vip_bought_date: {users[i][9]}
special_vip_links_number: {users[i][10]}
deadline_of_common_vip: {users[i][11]}
'''
        await message.answer(text=text_)
        await asyncio.sleep(0.1)

    await message.answer(text=f'Всего участников: {len(users)}')




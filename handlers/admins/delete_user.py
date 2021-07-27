from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from loader import dp, db_of_active_users
from states import DeleteUserByAdmin
import data.config
import datetime


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


@dp.message_handler(text='Удалить Участника')
async def add_user(message: types.Message, state: FSMContext):
    # добавления участника
    # Дынные: Telegram_id, Instagram_account_name, phone_number
    id = message.from_user.id

    if not check_admin(id):
        # пользователь не евляется админом
        await message.answer(text=f'Вы не админ. telegram_id={id}')
        return

    await DeleteUserByAdmin.choose_user.set()
    await message.answer('Введите instagram_account участника(_ для отмены):')


@dp.message_handler(state=DeleteUserByAdmin.choose_user)
async def add_user1_id(message: types.Message, state: FSMContext):
    instagram_account = message.text

    if instagram_account == '_':
        await message.answer('Вы отменили delete user')
        await state.finish()
        return
    try:
        db_of_active_users.delete_active_User_by_instagram_account_name(instagram_account)
        await message.answer('Пользователь успешно удалён')
    except Exception as er:
        await message.answer('Не удалось удолить пользователя')
        await message.answer(f'{er}')

    await state.finish()



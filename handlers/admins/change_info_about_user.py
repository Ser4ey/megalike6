from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from loader import dp, db_of_active_users
from states import ChangeInfoAboutUser
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


def get_user_text(user):
    try:
        text_ = f'''
__User__

telegram_id: {user[0]}
instagram_account_name: {user[1]}
phone_number: {user[2]}
registration_date: {user[3]}
available_links_for_today: {user[5]}
number_of_links_requested_today: {user[6]}
common_day_link_limit: {user[7]}
vip_status: {user[8]}
vip_bought_date: {user[9]}
special_vip_links_number: {user[10]}
deadline_of_common_vip: {user[11]}
'''
        return text_
    except Exception as er:
        return er


@dp.message_handler(text='Изменить информацию о пользователе')
async def change_info_about_user1(message: types.Message, state: FSMContext):
    id = message.from_user.id

    if not check_admin(id):
        # пользователь не евляется админом
        await message.answer(text=f'Вы не админ. telegram_id={id}')
        return

    await ChangeInfoAboutUser.choose_user.set()
    await message.answer('Введите instagram пользователя (Для отмены:_)')


@dp.message_handler(state=ChangeInfoAboutUser.choose_user)
async def change_info_about_user2(message: types.Message, state: FSMContext):
    instagram_account = message.text

    if instagram_account == '_':
        await message.answer('Вы отменили изменение информации о пользователе')
        await state.finish()
        return

    await state.update_data(instagram_account=instagram_account)

    user = db_of_active_users.select_active_User(instagram_account_name=instagram_account)
    if user is None:
        await message.answer(f'Такого пользователя не существует')
        await state.finish()
        return

    await state.update_data(instagram_account_name=instagram_account)


    text_ = f'''
1) Инстаграм аккаунт: {user[1]}
2) Номер телефона: {user[2]}
3) Лимит ссылок: {user[7]}
4) VIP статус: {user[8]}
not-vip(1) time-vip(2) special-vip(3)
5) Срок VIP: {user[11]}
При изменении срока випа меняется
дата его покупки(сегодня)
'''
    await message.answer(text_)

    await ChangeInfoAboutUser.choose_thing_to_change.set()


@dp.message_handler(state=ChangeInfoAboutUser.choose_thing_to_change)
async def change_info_about_user3(message: types.Message, state: FSMContext):
    thing_to_change = message.text

    try:
        thing_to_change = int(thing_to_change)
        if 1 > thing_to_change or thing_to_change > 5:
            await message.answer(f'Нужно ввести число от 1 до 5, попробуйте ещё раз')
            return
    except Exception as er:
        await message.answer(f'Информация не изменена: {er}')
        await state.finish()
        return

    values = ['Инстаграм аккаунт', 'Номер телефона', 'Лимит ссылок', 'VIP статус', 'Срок VIP']
    await message.answer(f'Укажите новое значение для "{values[thing_to_change-1]}"')

    await state.update_data(thing_to_change=thing_to_change)
    await ChangeInfoAboutUser.choose_value_to_change.set()


@dp.message_handler(state=ChangeInfoAboutUser.choose_value_to_change)
async def change_info_about_user3(message: types.Message, state: FSMContext):
    value_to_change = message.text

    if value_to_change == '_':
        await message.answer(f'Информация не изменена')
        await state.finish()
        return

    data_ = await state.get_data()
    thing_to_change = int(data_.get('thing_to_change'))
    instagram_account_name = data_.get('instagram_account_name')
    value_to_change = value_to_change

    keys_ = ['instagram_account_name', 'phone_number', 'common_day_link_limit', 'vip_status', 'deadline_of_common_vip']
    values = ['Инстаграм аккаунт', 'Номер телефона', 'Лимит ссылок', 'VIP статус', 'Срок VIP']

    if thing_to_change == 3:
        # проверка, чтоб лимит ссылок был числом
        try:
            value_to_change = int(value_to_change)
        except Exception as er:
            await message.answer(f'Информация не изменена')
            await message.answer(f'Нужно указать цифру')
            await message.answer(f'{er}')
            await state.finish()
            return
    elif thing_to_change == 5:
        # меняем дату покупки випа
        time_today = str(datetime.datetime.today()).strip().split('.')[0]
        db_of_active_users.update_any_info_about_any_active_User(
            instagram_account_name=instagram_account_name,
            thing_to_change='deadline_of_common_vip',
            new_data=time_today
        )


    db_of_active_users.update_any_info_about_any_active_User(
        instagram_account_name=instagram_account_name,
        thing_to_change=keys_[thing_to_change-1],
        new_data=value_to_change
    )

    await message.answer('Информация успешно изменена')
    user_text = get_user_text(db_of_active_users.select_active_User(instagram_account_name=instagram_account_name))
    await message.answer(user_text)
    await state.finish()




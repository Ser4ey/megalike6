from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from loader import dp, db_of_active_users
from states import DailyCheck
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


@dp.message_handler(text='Опубликовать проверку')
async def add_user(message: types.Message, state: FSMContext):
    # добавления участника
    # Дынные: Telegram_id, Instagram_account_name, phone_number
    id = message.from_user.id

    if not check_admin(id):
        # пользователь не евляется админом
        await message.answer(text=f'Вы не админ. telegram_id={id}')
        return

    await DailyCheck.send_big_text.set()
    await message.answer('Отправте результат проверки одним текстовым сообщением (_ для отмены).')


@dp.message_handler(state=DailyCheck.send_big_text)
async def add_user1_id(message: types.Message, state: FSMContext):
    big_text = message.text

    if big_text == '_':
        await message.answer('Вы отменили ежедневную проверку!')
        await state.finish()
        return

    await state.update_data(big_text=big_text)

    all_user = db_of_active_users.select_active_User()

@dp.message_handler(state=AddUserByAdmin.state_instagram_name)
async def add_user1_id(message: types.Message, state: FSMContext):
    instagram_account = message.text

    if instagram_account == '_':
        await message.answer('Вы отменили добавление пользователя')
        await state.finish()
        return

    user_info = db_of_active_users.select_active_User(instagram_account_name=instagram_account)
    if not user_info is None:
        await message.answer(f'Такой инстаграм аккаунт уже существует!')
        await state.finish()
        return

    await state.update_data(instagram_account=instagram_account)
    await message.answer('Добавления пользователя-3\n(Для отмены:_ Если нет, то:1)\nВведите номер телефона:')
    await AddUserByAdmin.state_phone_number.set()


@dp.message_handler(state=AddUserByAdmin.state_phone_number)
async def add_user1_id(message: types.Message, state: FSMContext):
    phone_number = message.text

    if phone_number == '_':
        await message.answer('Вы отменили добавление пользователя')
        await state.finish()
        return
    if str(phone_number) == '1':
        phone_number = '123-no-phone'

    data_ = await state.get_data()
    telegram_id = data_.get('telegram_id')
    instagram_account = data_.get('instagram_account')
    phone_number = phone_number
    time_today = str(datetime.datetime.today()).strip().split('.')[0]

    f_text = f'''
telegram_id: {telegram_id}
instagram_account: {instagram_account}
phone_number: {phone_number}
time_today: {time_today}
    '''
    await message.answer(f_text)
    await message.answer('Пользователь успешно добавлен!')
    await state.finish()
    db_of_active_users.add_active_User(
        telegram_id=telegram_id,
        instagram_account_name=instagram_account,
        phone_number=phone_number,
        registration_date=time_today,

    )






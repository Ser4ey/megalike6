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
async def daily2(message: types.Message, state: FSMContext):
    big_text = message.text

    if big_text == '_':
        await message.answer('Вы отменили ежедневную проверку!')
        await state.finish()
        return

    await state.update_data(big_text=big_text)
    Users = []

    all_user = db_of_active_users.select_all_active_Users()
    List_of_id = 's:'

    for i in range(len(all_user)):
        vip_status = all_user[i][8]
        if 'vip' in vip_status or 'VIP' in vip_status or 'Vip' in vip_status:
            continue
        telegram_id = all_user[i][0]
        instagram_account = all_user[i][1]
        Users.append((telegram_id, instagram_account))

    text_answer = '---------------\n\n'
    for i in range(len(Users)):
        telegram_id = Users[i][0]
        instagram_account = Users[i][1]

        text_ = f'{i}) {telegram_id} -> {instagram_account}'
        text_answer = text_answer + text_ + '\n'

        List_of_id = List_of_id + ':' + str(telegram_id)

    List_of_id = List_of_id.strip(':')
    List_of_id = List_of_id.strip('s:')
    await message.answer(text_answer)
    await message.answer(f'Укажите через ":" номера пользователей, которые не прошли задания')
    await state.update_data(List_of_id=List_of_id)

    await DailyCheck.info_by_users.set()


@dp.message_handler(state=DailyCheck.info_by_users)
async def daily2(message: types.Message, state: FSMContext):
    user_text = message.text
    user_text = user_text.strip()
    user_text = user_text.strip(':')
    user_text = user_text.strip('s:')


    data_ = await state.get_data()
    big_text = data_.get('big_text')
    List_of_id = data_.get('List_of_id')


    users = db_of_active_users.select_all_active_Users()
    for user in users:
        try:
            user_id_ = user[0]
            await dp.bot.send_message(chat_id=user_id_, text=big_text)
        except:
            pass

    list_of_user = List_of_id.split(':')
    list_of_targets = user_text.split(':')

    for target in list_of_targets:
        try:
            # print(f'target: {target}')
            # print(f'target: {list_of_user[int(target)]}')

            await dp.bot.send_message(chat_id=list_of_user[int(target)], text='Вы не прошли проверку сегодня!')
        except:
            await message.answer(f'Не удалось отправить сообщение: {target}')

    await state.finish()






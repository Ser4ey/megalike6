import sqlite3

from aiogram import types

from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from loader import dp, db, User_and_Exists
from states.change_ins_account import ChangAccount
from keyboards.default.main_menu import main_menu
from keyboards.default import main_menu
from keyboards.inline.yes_or_no import yes_or_no_inline
from utils.PaseR.inst_parser import wait_your_turn, find_best
from keyboards.inline.settings import settings_keyboard



# def valid_account(sab, posts):
#     try:

@dp.message_handler(text='Настройки')
async def setting_list(message: types.Message, state: FSMContext):

    await message.answer(text=f'''Настройки:''', reply_markup=settings_keyboard)



@dp.callback_query_handler(text='chat_to_account_h')
async def not_user_account(call: CallbackQuery, state: FSMContext):
    await call.answer()

    text = '''
Введите ваш инстаграм аккаунт в формате @nickname
Требования к аккаунту:
1)Минимум 5 постов
2)Минимум 20 подписчиков
-------------------------
Для отмены введите 1'''
    await call.message.answer(text=text, reply_markup=ReplyKeyboardRemove())

    await ChangAccount.change1.set()


@dp.callback_query_handler(text='chat_to_account_h')
async def change_acc1(call: CallbackQuery, state: FSMContext):
    await call.answer()

    text = '''
Введите ваш инстаграм аккаунт в формате @nickname
Требования к аккаунту:
1)Минимум 5 постов
2)Минимум 20 подписчиков
-------------------------
Для отмены введите 1'''
    await call.message.answer(text=text, reply_markup=ReplyKeyboardRemove())

    await ChangAccount.change1.set()




@dp.message_handler(state=ChangAccount.change1)
async def continue_reg3(message: types.Message, state: FSMContext):
    message_text = message.text

    if message_text == '1' or message_text == 1:
        await state.finish()
        await message.answer('Вы отменили добавление аккаунта', reply_markup=main_menu)
        return

    await state.update_data(inst_akk=message_text)
    # проверка аккаунта
    await message.answer(text='Проверяем аккаунт ...')

    parser = find_best(User_and_Exists)
    await wait_your_turn(parser)


    if message_text[0] == '@':
        message_text = message_text[1:]

    account = await parser.parse_user_without_search(message_text)
    parser.queue = parser.queue[1:]

    if account is None:
        await message.answer(text='Такого аккаунта не существует!\nУкажите другой.')
        return


    text = f'Имя аккаунта: @{message_text}' + '\n'

    for key, vall in account.items():
        t = f'Количество {key}: {vall}' + '\n'
        text += t
        print(text)
    text += f'Ссылка: https://instagram.com/{message_text}/' + '\n'

    try:
        print(account)
        post1 = int(account['Постов'])
        sabbs = int(account['Подписчиков'])

        if post1 < 5 or sabbs < 25:
            text += 'Этот аккаунт не подходит, укажите другой.'
            await message.answer(text=text)
            return

    except:
        print('Account ok')


    text += '\n' + 'Это ваш аккаунт?'


    await message.answer(text=text, reply_markup=yes_or_no_inline)

    await state.update_data(id=message.from_user.id)
    await state.update_data(instagram_account=message_text)

    await ChangAccount.f_change.set()


@dp.callback_query_handler(text='no', state=ChangAccount.f_change)
async def not_user_account(call: CallbackQuery, state: FSMContext):
    await call.answer()

    text = 'Вы не поменяли аккаунт.'
    await call.message.answer(text=text, reply_markup=main_menu)
    await state.finish()



@dp.callback_query_handler(text='yes', state=ChangAccount.f_change)
async def user_account(call: CallbackQuery, state: FSMContext):
    await call.answer()

    data = await state.get_data()

    user_id =  data.get('id')
    account = data.get('instagram_account')

    db.update_instagram_akk(id=user_id, instagram_akk=account)
    await call.message.answer(text=f'Вы успешно изменили свой аккаунт на {account}', reply_markup=main_menu)
    await state.finish()
    db_info = db.select_user(id=user_id)

    # await call.message.answer(text=db_info)
    print('!!! ======== !!!Пользователь сменил аккаунт!!! ======== !!!')
    print(db_info)
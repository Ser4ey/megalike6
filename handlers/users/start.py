import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from loader import dp, db, User_and_Exists
from states import Start_new_user_reg
from keyboards.default import start_menu, start_menu2
from keyboards.default import main_menu
from utils.PaseR.inst_parser import wait_your_turn, find_best
from keyboards.inline.yes_or_no import yes_or_no_inline



# def valid_account(sab, posts):
#     try:

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):

    name = message.from_user.full_name
    id = message.from_user.id

    if not db.select_user(id=id) == None:
        await message.answer(r'Вы открыли главное меню по команде /start', reply_markup=main_menu)
        await Start_new_user_reg.problem_fix.set()
        await state.finish()
        return

    await message.answer(text=f'''
Привет 👋! Это бот активности для Instagram.
С помощью этого бота вы сможете получать лайки и комментарии на свои посты.
Жми на кнопку "Расскажи правила"
    ''', reply_markup=start_menu)

    try:
        db.add_user(id=id, name=name, balance=0)
    except sqlite3.IntegrityError as err:
        print(err)

    await Start_new_user_reg.st1.set()


@dp.message_handler(state=Start_new_user_reg.st1)
async def continue_reg(message: types.Message, state: FSMContext):

    text = '''Как это работает? 
1) Вы получаете ссылку на пост
2) Переходите по ссылке и оставляете комментарий ПО ТЕМЕ и от 4 слов 
3) Ставите лайк на пост
4) Возвращаетесь в бота и жмёте на кнопку проверить
5) Бот проверяет и зачисляет вам 1 балл.
6) Этот балл вы можете потратить на свои задания и получить активность на свой пост

1 балл - 1 комментарий и лайк на ваш пост
Вы можете купить баллы по курсу 1 балл = 2 рубля

Жми на кнопку и регистрируйся!'''

    await message.answer(text=text, reply_markup=start_menu2)
    await Start_new_user_reg.st2.set()


@dp.message_handler(state=Start_new_user_reg.st2)
async def continue_reg2(message: types.Message, state: FSMContext):
    text = '''    
Введите ваш инстаграм аккаунт в формате @nickname
Требования к аккаунту:
1)Минимум 5 постов
2)Минимум 20 подписчиков
    '''
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await Start_new_user_reg.st3.set()


@dp.message_handler(state=Start_new_user_reg.st3)
async def continue_reg3(message: types.Message, state: FSMContext):
    message_text = message.text
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

    await Start_new_user_reg.confirm_account.set()


@dp.callback_query_handler(text='no', state=Start_new_user_reg.confirm_account)
async def not_user_account(call: CallbackQuery, state: FSMContext):
    await call.answer()

    text = 'Введите ваш инстаграм аккаунт в формате @nickname'
    await call.message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await Start_new_user_reg.st3.set()



@dp.callback_query_handler(text='yes', state=Start_new_user_reg.confirm_account)
async def user_account(call: CallbackQuery, state: FSMContext):
    await call.answer()

    data = await state.get_data()

    user_id =  data.get('id')
    account = data.get('instagram_account')

    db.update_instagram_akk(id=user_id, instagram_akk=account)
    await call.message.answer(text='Вы успешно зарегистрировались', reply_markup=main_menu)
    await state.finish()
    db_info = db.select_user(id=user_id)

    # await call.message.answer(text=db_info)
    print('!!! ======== !!!Зарегистрировался новый пользователь!!! ======== !!!')
    print(db_info)

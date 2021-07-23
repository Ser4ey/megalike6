from utils.PaseR.inst_parser import wait_your_turn, find_best
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from loader import dp, db, db_tasks, db_active_tasks, db_gen_id, User_and_Exists
from keyboards.default import main_menu
from states import AddTask
from keyboards.default import cancel_menu
from keyboards.inline.task_without_comment import no_comment


def check_to_cancel(text):
    if text == 'Отменить' or text == '!':
        return True
    else:
        return False


def check_link_to_repeat(task_link, user_id):
    tasks = db_tasks.select_task(users_which_done_post=task_link)
    if tasks is None:
        return str(user_id)

    tasks_set = set()
    for task in tasks:
        a = task[4]
        a = a.split(':')

        if len(a) == 0:
            continue

        for i in range(len(a)):
            tasks_set.add(a[i])

    if len(tasks_set) == 0:
        return str(user_id)

    tasks_set = list(tasks_set)
    tasks_set = ':'.join(tasks_set)
    tasks_set = str(tasks_set) + ':' + str(user_id)

    if tasks_set[0] == ':':
        tasks_set = tasks_set[1:]

    return tasks_set


@dp.message_handler(text='Добавить пост')
async def add_task(message: types.Message, state: FSMContext):
    id = message.from_user.id
    balance = db.select_user(id=id)[3]
    if int(balance) > 0:
        await message.answer(text=f'''
        У тебя, {balance} балов!\nДобавь ссылку на пост в формате:\n https://instagram.com\n
        ''', reply_markup=cancel_menu)
        await state.update_data(balance=balance)
        await state.update_data(id=id)
        await AddTask.link_1.set()
        return
    else:
        await message.answer(text='Вам нужен, хотя бы 1 балл. Выполняйте задания или купите баллы.', reply_markup=main_menu)


@dp.message_handler(state=AddTask.link_1)
async def check_link(message: types.Message, state: FSMContext):
    src = message.text

    if check_to_cancel(src):
        await message.answer(text='Вы отменили добавление поста', reply_markup=main_menu)
        await state.finish()
        return

    await message.answer(text='Проверяем пост, это может занять немного времени...')
    #

    if len(src) < 26:

        await message.answer(text='Не корректная ссылка!')
        return

    parser = find_best(User_and_Exists)
    await wait_your_turn(parser)

    try:
        result = await parser.is_post_exist(src)
        parser.queue = parser.queue[1:]
    except:
        await message.answer(text='Не корректная ссылка!')
        result = None
        parser.queue = parser.queue[1:]
        return

    if result is None:
        result = False

    if result:
        data = await state.get_data()
        balance = data.get('balance')
        text = f'Пост добавлен. Сколько баллов вы хотите потратить? (от 1 до {balance})'
        await message.answer(text=text)
        await state.update_data(src=src)
        await AddTask.balance_2.set()
    else:
        text = 'Ваша ссылка не действительна, укажите другую'
        await message.answer(text=text)


@dp.message_handler(state=AddTask.balance_2)
async def check_balance(message: types.Message, state: FSMContext):
    task_balance = message.text

    if check_to_cancel(task_balance):
        await message.answer(text='Вы отменили добавление поста', reply_markup=main_menu)
        await state.finish()
        return


    # проверка

    if task_balance.isdigit():
        task_balance = int(task_balance)
        data = await state.get_data()
        user_balance = data.get('balance')
        user_balance = int(user_balance)

        if task_balance > user_balance:
            await message.answer('У вас не достаточно баллов, укажите число меньше!', reply_markup=cancel_menu)
            return
        if task_balance == 0:
            await message.answer('Минимальный баланс задания 1 балл, укажите друго число!', reply_markup=cancel_menu)
            return

        await AddTask.comment_3.set()
        await state.update_data(task_balance=task_balance)

        await message.answer(text=f'Добавьте примечание к вашему заданию.\nИли нажмите на кнопкку!', reply_markup=no_comment)
    else:
        await message.answer(text='Укажите целое число.', reply_markup=cancel_menu)


@dp.callback_query_handler(text='add_task_without_comment', state=AddTask.comment_3)
async def without_comm(call: CallbackQuery, state: FSMContext):
    await call.answer()

    # add task

    data = await state.get_data()
    user_id = data.get('id')
    task_balance = data.get('task_balance')
    user_balance = data.get('balance')
    task_balance = int(task_balance)
    task_link = data.get('src')
    task_id = db_gen_id.gen_id()
    author_comment = 'Оставте осмысленный коментарий более 4 слов!'
    users_which_done_task = check_link_to_repeat(task_link, user_id)


#     нужно добавить проверку на повторные ссылки (добавлено)
    await call.message.answer(text='Ваше задание добавляется, это может занять время!', reply_markup=main_menu)
    db_tasks.add_task(id=task_id, src=task_link, balance=task_balance, author=user_id, users_which_done_post=users_which_done_task, author_comment=author_comment)
    db_active_tasks.add_active_task_from_task(id=task_id)

    # добавление задания пользователю, в его задания
    db.add_task_to_user_tasks(id=user_id, task=task_id)
    #

    await call.message.answer(text='Ваше задание успешно добавлено, без комментариев!', reply_markup=main_menu)
    db.update_user_balance_with_const(id=user_id, change_to=(-task_balance))

    new_balance = user_balance - task_balance
    await call.message.answer(text=f'Ваш баланс {new_balance} баллов.')

    await state.finish()


@dp.message_handler(state=AddTask.comment_3)
async def add_comment(message: types.Message, state: FSMContext):
    comment = message.text

    if check_to_cancel(comment):
        await message.answer(text='Вы отменили добавление поста', reply_markup=main_menu)
        await state.finish()
        return

    # add task

    data = await state.get_data()
    user_id = data.get('id')
    task_balance = data.get('task_balance')
    user_balance = data.get('balance')
    task_balance = int(task_balance)
    task_link = data.get('src')
    task_id = db_gen_id.gen_id()
    author_comment = comment
    users_which_done_task = check_link_to_repeat(task_link, user_id)


#     нужно добавить проверку на повторные ссылки (добавлено)

    await message.answer(text='Ваше задание добавляется, это может занять время!', reply_markup=main_menu)
    db_tasks.add_task(id=task_id, src=task_link, balance=task_balance, author=user_id, users_which_done_post=users_which_done_task, author_comment=author_comment)
    db_active_tasks.add_active_task_from_task(id=task_id)

    # добавление задания пользователю, в его задания
    db.add_task_to_user_tasks(id=user_id, task=task_id)
    #

    await message.answer(text='Ваше задание успешно добавлено, c комментарием!', reply_markup=main_menu)
    db.update_user_balance_with_const(id=user_id, change_to=(-task_balance))

    new_balance = user_balance - task_balance
    await message.answer(text=f'Ваш баланс {new_balance} баллов.')

    await state.finish()




#
#

from aiogram import types, Dispatcher, Bot
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from loader import dp, db, db_tasks, db_active_tasks, db_gen_id, Parsing_Posts, Parse_Comments
from keyboards.default import main_menu
import time
from threading import Timer
import asyncio
from states.doing_task import DoTask
from keyboards.inline.under_task import under_task
from utils.PaseR.inst_parser import find_best, wait_your_turn



def future_check(user_id, task_id):
    task = db_active_tasks.select_active_task(id=task_id)
    user_id = str(user_id)

    if task is None:
        return
    if user_id in task[3].split(':'):
        return
    if user_id in task[3]:
        return

    user = db.select_user(id=user_id)
    last_a = user[7]

    # if str(time_task) in last_a:
    #     return

    t = str(time.time())
    t = '-2'+':' + t
    db.update_user_last_activity(id=user_id, last_activity=t)

    db_active_tasks.update_active_limit1(id=task_id, change_to=1)



def get_a_task(done_tasks, user_id):
    tasks = db_active_tasks.select_all_active_tasks_which_user_not_done(done_tasks)

    if tasks is None:
        return None

    user_id = str(user_id)

    for i in tasks:
        if i[4] < 1:
            continue

        if user_id in i[3]:
            continue

        if user_id in i[3].split(':'):
            continue

        return i

    return None


async def check_task12(task_id1, inst_akk1):
    parser = find_best(Parsing_Posts)
    await wait_your_turn(parser)

    problems = [True, True, True, 25]
    link = db_tasks.select_task(id=task_id1)
    link = link[1]
    inst_akk1 = str(inst_akk1)

    print('lake was parsering')

    try:
        user_which_like = await parser.find_liked_users_from_olegS(link)
        # parser.queue = parser.queue[1:]

        if str(inst_akk1) in user_which_like or str(inst_akk1) in ':'.join(user_which_like):
            problems[0] = True
        elif user_which_like == 'error123':
            problems[0] = True
        else:
            problems[0] = False
    except:
        print('Ошибка при проверке поста')

    try:

        # if '?' in link:
        #     link = link.split('?')[-1]

        dict_of_users_who_comment = await parser.find_comments_fromS(link)
        parser.queue = parser.queue[1:]


        # if dict_of_users_who_comment is None:
        #     problems[1] = False
        #     problems[2] = False
        #     problems[3] = 0

        if 'tl' in dict_of_users_who_comment.keys():
            return problems
        else:
            comment1 = [False, 0]
            for user, comment in dict_of_users_who_comment.items():
                if str(user).strip("@") == str(inst_akk1).strip("@"):
                    comment1[0] = True
                    l = int(len(comment))
                    if l > int(comment1[1]):
                        comment1 = l

            problems[1] = comment1[0]
            problems[3] = comment1[1]

            if problems[3] < 20:
                problems[2] = False

        return problems

    except:
        print('Ошибка при проверки поста на комментарий')

    return problems







def time_check(user_id):
    user = db.select_user(id=user_id)
    a = user[-1]
    if int(a.split(':')[0]) == (-2):
        return True
    else:
        return False



# +
@dp.message_handler(text='Задания')
async def get_task(message: types.Message, state: FSMContext):
    await state.finish()

    await message.answer(text='Подбираем для вас задание, подождите немного...', reply_markup=ReplyKeyboardRemove())

    id = message.from_user.id
    user = db.select_user(id=id)
    inst_akk = user[2]
    task = get_a_task(done_tasks=user[4], user_id=id)

    if task is None:
        await message.answer('К сожалению, пока нет доступных заданий!', reply_markup=main_menu)
        return

    last_activity = str(task[0]) + ':' + str(time.time())
    tasks_in_session = str(user[4]) + ':' + str(task[0])

    await state.update_data(task_id=task[0])
    await state.update_data(last_activity=last_activity)
    await state.update_data(tasks_in_session=tasks_in_session)
    await state.update_data(user_id=id)
    await state.update_data(inst_akk=inst_akk)



    db.update_user_last_activity(id=id, last_activity=last_activity)
    db_active_tasks.update_active_limit1(id=task[0], change_to=(-1))


    # text = f'баланс {task[2]}\nлимит {task[4]}\n src={task[1]}\n users{task[3]}'
    text = f'''
Твое задание: прочитать пост, поставить лайк и вдумчивый комментарий от 4 слов
Ссылка: {task[1]}

После выполнения жми «выполнено»
'''

    await message.answer(text=text, reply_markup=under_task)

    # вызов функции отложенной проверки

    t = Timer(1200, future_check, args=[id, task[0]])
    t.start()

    await DoTask.do1.set()




@dp.callback_query_handler(text='check_task', state=DoTask.do1)
async def check_task(call: CallbackQuery, state: FSMContext):

    await call.answer()

    data = await state.get_data()
    tasks_in_session = data.get('tasks_in_session')
    task_id = data.get('task_id')
    user_id = data.get('user_id')
    inst_akk = data.get('inst_akk')

    print('проверка', user_id)

    r = time_check(user_id)
    if r:
        t = str(time.time())
        last_activity = '-1' + ':' + t
        data = await state.get_data()
        user_id = data.get('user_id')
        task_id = data.get('task_id')
        db.update_user_last_activity(id=user_id, last_activity=last_activity)
        # db_active_tasks.update_active_limit1(id=task_id, change_to=1)
        await call.message.answer('Время истекло! Запросите задания снова!',reply_markup=main_menu)
        await state.finish()
        return



    await call.message.answer(text='Проверка задания.\nМожет занимать до 100 секунд.')
    await DoTask.checking_right_now.set()
    # проверка
    #

    result = await check_task12(task_id, inst_akk)

    t1 = f'{result[0]} {result[1]} {result[2]} {result[3]}'
    # await call.message.answer(text=t1)

    await DoTask.do1.set()

    if result[0] is None or result[1] is None or result[2] is None or result[0] == False or \
            result[1] == False or result[2] == False:

        #
        link2 = db_tasks.select_task(id=task_id)
        text2 = ''
        # try:
        #     # text2 += link2[1]
        #     # text2 += '\n'
        # except:
        #     pass
        #

        if result[0] is None or result[0] == False:
            text2 = text2 + 'Нет лайка на посту ❌' + '\n'
        else:
            text2 = text2 + 'Есть лайк на посту ✅' + '\n'

        if result[1] is None or result[1]:
            text2 = text2 + 'Есть комментарий на посту ✅' + '\n'

            if result[2]:
                text2 = text2 + 'Длина комментария ✅' +'\n'
            else:
                text2 = text2 + f'Комментарий слишком короткий: ({result[3]} символов из 20)' + '\n'
        else:
            text2 = text2 + 'Нет комментария на посту ❌' + '\n'

        text2 += r'Вы не выполнили все условия ❌. Исправьте и нажмите кнопку "Проверить"!'

        await call.message.answer(text=text2, reply_markup=under_task)

        return



    db.update_user_balance_with_const(id=user_id, change_to=1)
    db.update_done_tasks(id=user_id, task_id=task_id)
    if str(task_id) not in tasks_in_session.split(':'):
        tasks_in_session += ':' + str(task_id)


    task = db_active_tasks.select_active_task(id=task_id)

    if task is None:
        print('Ошибка, невозможно обновить информацию о задании.')
    else:
        db_active_tasks.update_active_balance(id=task_id, change_to=(-1))
        db_active_tasks.update_user_which_done_active_post(id=task_id, user_id=user_id)
        task = db_active_tasks.select_active_task(id=task_id)

        if int(task[2]) < 1:
            db_active_tasks.delete_active_task(id=task_id)


    user = db.select_user(id=user_id)
    balance = user[3]
    await call.message.answer(text=f'Отлично 👍! Вы получили 1 балл.\nВаш баланс {balance}')


#     новое задание


    id = user_id
    await call.message.answer(text='Подбираем для вас новое задание, подождите немного...', reply_markup=ReplyKeyboardRemove())

    # id = message.from_user.id
    # user = db.select_user(id=id)
    # inst_akk = user[2]
    task = get_a_task(done_tasks=user[4], user_id=id)

    if task is None:
        await call.message.answer('К сожалению, пока нет доступных заданий!', reply_markup=main_menu)
        await state.finish()
        return

    last_activity = str(task[0]) + ':' + str(time.time())
    tasks_in_session = str(user[4]) + ':' + str(task[0])

    await state.update_data(task_id=task[0])
    await state.update_data(last_activity=last_activity)
    await state.update_data(tasks_in_session=tasks_in_session)
    # await state.update_data(user_id=id)
    # await state.update_data(inst_akk=inst_akk)



    db.update_user_last_activity(id=id, last_activity=last_activity)
    db_active_tasks.update_active_limit1(id=task[0], change_to=(-1))

    # text = f'баланс {task[2]}\nлимит {task[4]}\n src={task[1]}\n users{task[3]}'
    text = f'баланс {task[2]}\nлимит {task[4]}\n src={task[1]}\n users{task[3]}'
    await call.message.answer(text=text, reply_markup=under_task)

    # вызов функции отложенной проверки

    t = Timer(1200, future_check, args=[id, task[0]])
    t.start()

    await DoTask.do1.set()





# +
@dp.callback_query_handler(text='skip_task', state=DoTask.do1)
async def skip_task(call: CallbackQuery, state: FSMContext):
    await call.answer()

    data = await state.get_data()
    tasks_in_session = data.get('tasks_in_session')
    task_id = data.get('task_id')
    user_id = data.get('user_id')

    r = time_check(user_id)
    if r:
        t = str(time.time())
        last_activity = '-1' + ':' + t
        data = await state.get_data()
        user_id = data.get('user_id')
        task_id = data.get('task_id')
        db.update_user_last_activity(id=user_id, last_activity=last_activity)
        # db_active_tasks.update_active_limit1(id=task_id, change_to=1)
        await call.message.answer('Время истекло! Запросите задания снова!', reply_markup=main_menu)
        await state.finish()
        return

    # добавление пользователя в задание и изменение лимита
    db_active_tasks.update_user_which_done_active_post(id=task_id, user_id=user_id)
    db_active_tasks.update_active_limit1(id=task_id, change_to=1)

    task = get_a_task(done_tasks=tasks_in_session, user_id=user_id)

    if task is None:
        await call.message.answer(text='К сожалению, пока нет доступных заданий!', reply_markup=main_menu)
        await state.finish()
        return

    last_activity = str(task[0]) + ':' + str(time.time())
    tasks_in_session = tasks_in_session + ':' + str(task[0])

    await state.update_data(task_id=task[0])
    await state.update_data(last_activity=last_activity)
    await state.update_data(tasks_in_session=tasks_in_session)

    db.update_user_last_activity(id=user_id, last_activity=last_activity)
    db_active_tasks.update_active_limit1(id=task[0], change_to=(-1))

    await call.message.answer(task, reply_markup=under_task)

    # отложенная проверка
    t = Timer(1200, future_check, args=[user_id, task[0]])
    t.start()

    await DoTask.do1.set()
    # await state.finish()

# +
@dp.callback_query_handler(text='cancel_task', state=DoTask.do1)
async def stop_task(call: CallbackQuery, state: FSMContext):
    await call.answer()

    t = str(time.time())
    last_activity = '-1' + ':' + t
    data = await state.get_data()
    user_id = data.get('user_id')
    task_id = data.get('task_id')

    r = time_check(user_id)
    if r:
        t = str(time.time())
        last_activity = '-1' + ':' + t
        data = await state.get_data()
        user_id = data.get('user_id')
        task_id = data.get('task_id')
        db.update_user_last_activity(id=user_id, last_activity=last_activity)
        # db_active_tasks.update_active_limit1(id=task_id, change_to=1)
        await call.message.answer('Время истекло! Запросите задания снова!',reply_markup=main_menu)
        await state.finish()
        return



    db.update_user_last_activity(id=user_id, last_activity=last_activity)
    db_active_tasks.update_active_limit1(id=task_id, change_to=1)

    await call.message.answer('Вы прекратили выполнение заданий.\nЧто вы хотите сделать дальше?', reply_markup=main_menu)
    await state.finish()



@dp.message_handler(state=DoTask.checking_right_now)
async def get_task(message: types.Message, state: FSMContext):
    await message.answer(text='Мы проверяем пост, пожалуйста подождите.')
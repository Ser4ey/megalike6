import asyncio
import sqlite3
import threading

from aiogram import types, Dispatcher, Bot
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from loader import dp, db, db_tasks, db_active_tasks, db_gen_id, bot
from keyboards.default import main_menu
import time
from threading import Timer
import asyncio
from states.doing_task import DoTask
from keyboards.inline.under_task import under_task

# def hello(db):
#     asyncio.run(u7(db))
#
#
# async def u7(db):
#     a = db.gen_id()
#     print(a)
#     await asyncio.sleep(2)
#     print(a)


def future_check(user_id, task_id):
    task = db_active_tasks.select_active_task(id=task_id)
    if task is None:
        return
    if user_id in task[3].split(':'):
        return

    t = str(time.time())
    t = '-2'+':' + t
    db.update_user_last_activity(id=user_id, last_activity=t)


def get_a_task(done_tasks, user_id):
    tasks = db_active_tasks.select_all_active_tasks_which_user_not_done(done_tasks)

    if tasks is None:
        return None

    for i in tasks:
        if i[4] < 1:
            continue
        if user_id in i[3].split(':'):
            continue

        return i

    return None


def check_task(task_id, inst_akk):
    return True



def time_check(user_id):
    user = db.select_user(id=user_id)
    a = user[-1]
    if int(a.split(':')[0]) == (-2):
        return True
    else:
        return False




@dp.message_handler(text='Задания')
async def get_task(message: types.Message, state: FSMContext):
    await state.finish()

    await message.answer(text='Подбираем для вас задание подождите немного...', reply_markup=ReplyKeyboardRemove())

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

    t = Timer(10, future_check, args=[id, task[0]])
    t.start()

    db.update_user_last_activity(id=id, last_activity=last_activity)
    db_active_tasks.update_active_limit1(id=task[0], change_to=(-1))

    await message.answer(task, reply_markup=under_task)

    # вызов функции отложенной проверки

    await DoTask.do1.set()




@dp.callback_query_handler(text='check_task', state=DoTask.do1)
async def check_task(call: CallbackQuery, state: FSMContext):
    await call.answer()

    data = await state.get_data()
    tasks_in_session = data.get('tasks_in_session')
    task_id = data.get('task_id')
    user_id = data.get('user_id')
    inst_akk = data.get('inst_akk')

    r = time_check(user_id)
    if r:
        t = str(time.time())
        last_activity = '-1' + ':' + t
        data = await state.get_data()
        user_id = data.get('user_id')
        task_id = data.get('task_id')
        db.update_user_last_activity(id=user_id, last_activity=last_activity)
        db_active_tasks.update_active_limit1(id=task_id, change_to=1)
        await call.message.answer('Время истекло! Запросите задания снова!',reply_markup=main_menu)
        await state.finish()
        return

    # user = db.select_user(id=user_id)
    # if task_id in user[4].split(':'):
    #     await call.message.answer('Вы уже прошли это задание')
    #     return
    # Обратить внимание на мульти выполнение одного задания


    # result = check_task(task_id=task_id, inst_akk=inst_akk)
    result = True
    if not result:
        await call.message.answer(text='Вы не прошли задание')
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
        #     await call.message.answer("333")
        # else:
        #     await call.message.answer('33334')



    user = db.select_user(id=user_id)
    balance = user[3]
    await call.message.answer(text=f'Вы получили 1 бал! Ваш баланс {balance}')

#     новое задание
    task = get_a_task(done_tasks=tasks_in_session, user_id=user_id)
    if task is None:
        await call.message.answer(text=f'К сожалению заданий больше нет!', reply_markup=main_menu)
        t = str(time.time())
        last_activity = '-1' + ':' + t
        db.update_user_last_activity(id=user_id, last_activity=last_activity)
        await state.finish()
    else:

        last_activity = str(task[0]) + ':' + str(time.time())
        task_id = task[0]
        if str(task_id) not in tasks_in_session.split(':'):
            tasks_in_session += ':' + str(task_id)


        await state.update_data(task_id=task[0])
        await state.update_data(last_activity=last_activity)
        await state.update_data(tasks_in_session=tasks_in_session)
        await state.update_data(inst_akk=inst_akk)
#
        db.update_user_last_activity(id=user_id, last_activity=last_activity)
        db_active_tasks.update_active_balance(id=task[0], change_to=(-1))

        await call.message.answer(task, reply_markup=under_task)


        t = Timer(10, future_check, args=[call.message.from_user.id, task[0]])
        t.start()







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
        db_active_tasks.update_active_limit1(id=task_id, change_to=1)
        await call.message.answer('Время истекло! Запросите задания снова!',reply_markup=main_menu)
        await state.finish()
        return



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
    t = Timer(10, future_check, args=[call.message.from_user.id, task[0]])
    t.start()

    await DoTask.do1.set()
    # await state.finish()


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
        db_active_tasks.update_active_limit1(id=task_id, change_to=1)
        await call.message.answer('Время истекло! Запросите задания снова!',reply_markup=main_menu)
        await state.finish()
        return



    db.update_user_last_activity(id=user_id, last_activity=last_activity)
    db_active_tasks.update_active_limit1(id=task_id, change_to=1)

    await call.message.answer('Вы прекратили выполнение заданий.\nЧто вы хотите сделать дальше?', reply_markup=main_menu)
    await state.finish()


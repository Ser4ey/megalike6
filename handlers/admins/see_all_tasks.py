import data.config
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from loader import dp, db_of_dayly_tasks
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


@dp.message_handler(text='Список Заданий')
async def add_task(message: types.Message, state: FSMContext):
    '''Отпраляет админу меню админа'''
    id = message.from_user.id

    if not check_admin(id):
        # пользователь не евляется админом
        await message.answer(text=f'Вы не админ. telegram_id={id}')
        return

    tasks = db_of_dayly_tasks.select_all_day_Task()
    for i in range(len(tasks)):
        text_ = f'{i+1}) {tasks[i]}'
        text_ = f'''
Task-{i+1}

instagram_link: {tasks[i][0]}
creator_telegram_id: {tasks[i][1]}
task_status: {tasks[i][2]}
created_time: {tasks[i][3]}
comment_to_task: {tasks[i][4]}
telegram_id_of_users_who_request_this_task: {tasks[i][5]}
'''
        await message.answer(text=text_)
        await asyncio.sleep(0.1)

    await message.answer(text=f'Всего заданий: {len(tasks)}')




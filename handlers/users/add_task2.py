from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from loader import dp, db_of_active_users, db_of_dayly_tasks
from states import AddTaskByUser


@dp.message_handler(text='Добавить пост')
async def add_task(message: types.Message, state: FSMContext):
    id = message.from_user.id
    name = message.from_user.full_name

    user_info = db_of_active_users.select_active_User(telegram_id=id)
    if user_info is None:
        await message.answer(f'Приветствую, {name}! Вам необходимо зарегистрироваться.\nВаш id: {id}')
        return

    available_links_for_today = user_info[5]
    if available_links_for_today < 1:
        await message.answer(f'Ваш лимит ссылок на сегодня: {available_links_for_today}')
        await message.answer(f'Вы опубликовали все доступные вам ссылки')
        return

    await message.answer(f'Ваш лимит ссылок на сегодня: {available_links_for_today}')
    await AddTaskByUser.task_link.set()
    await message.answer('Введите ссылку на ваше задание')
    await state.finish()


@dp.message_handler(state=AddTaskByUser.task_link)
async def check_link(message: types.Message, state: FSMContext):
    src = message.text






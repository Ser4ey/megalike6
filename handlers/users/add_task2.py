import datetime

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
async def get_link(message: types.Message, state: FSMContext):
    src = message.text

    comment_text = 'Напишите качественный комментарий от 4 слов. Без использования шаблонов, наподобие:' \
                   ' "крутой пост, очень интересно", "спасибо за информацию, сохранила пост" и тд'

    if not 'instagram' in src:
        await message.answer('Неверный формат ссылки')
        await state.finish()
        return
    if len(src) > 100 or len(src) < 20:
        await message.answer('Неверный формат ссылки')
        await state.finish()
        return

    await message.answer('Введите комментарий к заданию. Введите 1, чтоб использовать комментарий по умолчанию.\n'
                         ' Введите _ для отмены')
    await message.answer(f'комментарий по умолчанию:\n{comment_text}')
    await AddTaskByUser.description.set()

    await state.update_data(src=src)


@dp.message_handler(state=AddTaskByUser.task_link)
async def get_description(message: types.Message, state: FSMContext):
    description = message.text

    if description == '_':
        await message.answer('Вы отменили добавление задания')
        await state.finish()
        return
    if len(description) > 350:
        await message.answer('Максимальный размер описания - 350 символов. Пожалуйста укажите описание ещё раз,'
                             'предварительно сократив его.')
        return
    if str(description) == '1':
        description = 'Напишите качественный комментарий от 4 слов. Без использования шаблонов, наподобие:' \
                   ' "крутой пост, очень интересно", "спасибо за информацию, сохранила пост" и тд'

    await state.finish()

    data_ = await state.get_data()
    src = data_.get('src')
    description = str(description)
    telegram_id = message.from_user.id
    time_today = str(datetime.datetime.today()).strip().split('.')[0]

    user_info = db_of_active_users.select_active_User(telegram_id=id)
    if user_info is None:
        await message.answer(f'Вам необходимо зарегистрироваться.\nВаш id: {id}')
        return

    available_links_for_today = user_info[5]
    user_status = user_info[8]
    instagram_account_name = user_info[1]

    db_of_dayly_tasks.add_Day_Task(
        instagram_link=src,
        creator_telegram_id=telegram_id,
        task_status=user_status,
        created_time=time_today,
        comment_to_task=description
    )
    db_of_active_users.update_any_info_about_any_active_User(
        instagram_account_name=instagram_account_name,
        thing_to_change='available_links_for_today',
        new_data=int(available_links_for_today)-1
    )

    await message.answer('Вы испешно опубликовали задание')











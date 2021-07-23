from aiogram import types
from loader import dp, db, db_tasks, db_active_tasks


@dp.message_handler(text='Мои посты')
async def my_post(message: types.Message):
    id = message.from_user.id
    user = db.select_user(id=id)
    user_tasks = user[5]

    # await message.answer(text=user_tasks)

    user_tasks = user_tasks.split(':')
    print(user)

    if len(user_tasks) == 0:
        text = 'Сейчас у вас нет постов.\nДобавте новый пост прямо сейчас!'
        await message.answer(text=text)
        return

    user_tasks2 = []
    for i in user_tasks:
        if i == '':
            continue
        if i is None:
            continue

        user_tasks2.append(i)

    user_tasks = user_tasks2

    new_user_tasks = []

    for task_id in user_tasks:

        active_task = db_active_tasks.select_active_task(id=task_id)
        passive_task = db_tasks.select_task(id=task_id)

        text = ''

        if active_task is None or active_task == []:
            # await message.answer(text='1')
            progress = '100%'
            text = f'Задание #{passive_task[0]} ВЫПОЛНЕНО' + '\n' + f'Ссылка: {passive_task[1]}' + '\n' + f'Сделано:{passive_task[2]}' \
                    + r' из ' + f'{passive_task[2]}' + f' ({progress})'

        else:
            try:
                progress = (float(passive_task[2]) - float(active_task[2])) /  float(passive_task[2])  * 100
                progress = round(progress, 2)
                progress = str(progress) + '%'
            except:
                progress = '100.0%'


            text = f'Задание #{passive_task[0]}' + '\n' + f'Ссылка: {passive_task[1]}' + '\n' + f'Сделано:' \
                        f'{passive_task[2]-active_task[2]}'+ r'/' + f'{passive_task[2]}' + f' ({progress})'

            new_user_tasks.append(task_id)


        await message.answer(text=text)

    tasks = ':'.join(new_user_tasks)

    db.set_new_user_tasks(id=id, tasks=tasks)



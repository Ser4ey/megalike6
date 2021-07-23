from utils.set_bot_commands import set_default_commands
from loader import db, db_tasks, db_active_tasks, db_gen_id, Parse_Comments


async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify

    # создание бызы данных ниже
    try:
        db.create_table_users()
        # db.delete_all_users(confirm=True)
    except Exception as er:
        print(er)
        print('----------------------------Error----------------------------')

    # генерация id
    try:
        db_gen_id.create_table_gen_id()
        result = db_gen_id.select_id(name='id_gen')
        # db_gen_id.delete_all_id(confirm=True)
        if result is None:
            db_gen_id.add_id(id=9)
            print('База gen_id была создана.')
        else:
            print('База gen_id уже существует.')
    except Exception as er:
        print(er)
        print('----------------------------Error----------------------------')

    # генерация tasks
    try:
        db_tasks.create_table_tasks()
        print('Была создана таблица заданий')
    except Exception as er:
        print(er)
        print('----------------------------Error----------------------------')

    # генерация active tasks
    try:
        db_active_tasks.create_table_active_tasks()
        print('Была создана таблица активных заданий')
    except Exception as er:
        print(er)
        print('----------------------------Error----------------------------')

    # Создание таблицы аккаунтов
    # try:
    #     db_parser.create_table_accounts()
    #     print('Была создана таблица аккаунтов!')
    # except Exception as er:
    #     print(er)
    #     print('----------------------------Error----------------------------')

    # инициализация аккаунтов


    await on_startup_notify(dp)
    await set_default_commands(dp)



    # for i in Parse_Comments:
    #     src2 = 'https://www.instagram.com/p/CKwoVAOLrzV/?igshid=1q4sb72f4tgql'
    #     a = await i.find_comments_best_last_S(src2)
    #
    #     print(a)
    #     print('parse comments')


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)


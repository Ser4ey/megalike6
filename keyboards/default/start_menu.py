from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


start_menu_users = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text='Посмотреть пост'),
            KeyboardButton(text='Добавить пост')
        ],
        [
            KeyboardButton(text='Помощь'),
            KeyboardButton(text='Настройки')
        ]
    ],
    resize_keyboard=True
)


start_menu_admin = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text='Добавить Участника'),
            KeyboardButton(text='Удалить Участника')
        ],
        [
            KeyboardButton(text='Изменить информацию о пользователе'),
        ],
        [
            KeyboardButton(text='Список Участников'),
            KeyboardButton(text='Список Заданий')
        ],
        [
            KeyboardButton(text='Опубликовать проверку')
        ]
    ],
    resize_keyboard=True
)



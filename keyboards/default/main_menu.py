from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_menu = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text='Задания'),
            KeyboardButton(text='Добавить пост')
        ],
        [
            KeyboardButton(text='Помощь'),
            KeyboardButton(text='Настройки')
        ],
        [
            KeyboardButton(text='Мои посты'),
            KeyboardButton(text='Баланс')
        ]
    ],
    resize_keyboard=True
)

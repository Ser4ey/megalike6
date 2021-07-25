from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_menu = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text='Посмотреть Задания'),
            KeyboardButton(text='Добавить Задание')
        ],
        [
            KeyboardButton(text='Помощь'),
            KeyboardButton(text='Настройки')
        ]
    ],
    resize_keyboard=True
)



start_menu2 = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text='Зарегистрироваться!')
        ]
    ],
    resize_keyboard=True
)



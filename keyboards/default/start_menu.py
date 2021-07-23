from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_menu = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text='Расcкажи правила')
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

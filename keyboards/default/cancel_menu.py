from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


cancel_menu = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text='Отменить')
        ]
    ],
    resize_keyboard=True
)
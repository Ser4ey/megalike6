from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text='1 ctroka')
        ],
        [
            KeyboardButton(text='2 ctroka'),
            KeyboardButton(text='2.1 ctroka')
        ]
    ],
    resize_keyboard=True
)





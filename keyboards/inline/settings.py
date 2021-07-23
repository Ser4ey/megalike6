from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


settings_keyboard = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [

                                        InlineKeyboardButton(
                                           text='Поменять аккаунт',
                                           callback_data='chat_to_account_h'
                                        )

                                      ]

                                  ])
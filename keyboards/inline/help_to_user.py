from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


help_to_user1 = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [

                                        InlineKeyboardButton(
                                           text='Чат',
                                           callback_data='chat_to_help'
                                        ),

                                        InlineKeyboardButton(
                                            text='Тех. поддержка',
                                            callback_data='technical_support_to_help'
                                        )

                                      ]

                                  ])
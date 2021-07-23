from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


yes_or_no_inline = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [

                                        InlineKeyboardButton(
                                           text='Да',
                                           callback_data='yes'
                                        ),

                                        InlineKeyboardButton(
                                            text='Нет',
                                            callback_data='no'
                                        )

                                      ]
                                  ])


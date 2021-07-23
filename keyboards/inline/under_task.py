from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


under_task = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [

                                        InlineKeyboardButton(
                                           text='Проверить',
                                           callback_data='check_task'
                                        ),

                                        InlineKeyboardButton(
                                            text='Пропустить',
                                            callback_data='skip_task'
                                        )

                                      ],
                                      [

                                          InlineKeyboardButton(
                                              text='Отменить',
                                              callback_data='cancel_task'
                                          )

                                      ]
                                  ])



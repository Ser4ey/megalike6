from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


list_of_bay1 = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [

                                        InlineKeyboardButton(
                                           text='50 баллов',
                                           callback_data='b50'
                                        ),

                                        InlineKeyboardButton(
                                            text='100 баллов',
                                            callback_data='b100'
                                        )

                                      ],
                                      [

                                          InlineKeyboardButton(
                                              text='250 баллов',
                                              callback_data='b250'
                                          ),

                                          InlineKeyboardButton(
                                              text='500 баллов',
                                              callback_data='b500'
                                          )

                                      ],
                                      [

                                          InlineKeyboardButton(
                                              text='1000 баллов',
                                              callback_data='b1000'
                                          ),

                                          InlineKeyboardButton(
                                              text='2000 баллов',
                                              callback_data='b2000'
                                          )

                                      ]

                                  ])
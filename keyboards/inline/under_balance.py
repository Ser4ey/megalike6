from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


top_up_balance = InlineKeyboardMarkup(row_width=1,
                                  inline_keyboard=[
                                      [
                                        InlineKeyboardButton(
                                           text='Купить баллы!',
                                           callback_data='buy_points'
                                        )
                                      ]
                                  ])
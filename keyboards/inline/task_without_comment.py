from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


no_comment = InlineKeyboardMarkup(row_width=1,
                                  inline_keyboard=[
                                      [
                                        InlineKeyboardButton(
                                           text='Без примечаний',
                                           callback_data='add_task_without_comment'
                                        )
                                      ]
                                  ])

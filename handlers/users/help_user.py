from aiogram import types

from keyboards.default.main_menu import main_menu
from loader import dp, db
from keyboards.inline.help_to_user import help_to_user1
from aiogram.types import CallbackQuery




@dp.message_handler(text='Помощь')
async def bot_echo(message: types.Message):
    text1 = '''
Привет, как я могу тебе помочь?
1)Чат с участниками
2)Тех. поддержка
    '''
    await message.answer(text=text1, reply_markup=help_to_user1)


@dp.callback_query_handler(text='chat_to_help')
async def skip_task(call: CallbackQuery):
    await call.answer()

    text1 = 'Вступите в чат @megalike_bot'
    await call.message.answer(text=text1, reply_markup=main_menu)


@dp.callback_query_handler(text='technical_support_to_help')
async def skip_task(call: CallbackQuery):
    await call.answer()

    text1 = 'Обратитесь в тех поддержку'
    await call.message.answer(text=text1, reply_markup=main_menu)



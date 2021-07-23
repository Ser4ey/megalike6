from aiogram import types
from loader import dp, db
from keyboards.inline.under_balance import top_up_balance
from aiogram.types import CallbackQuery
from keyboards.inline.list_of_buy import list_of_bay1





@dp.message_handler(text='Баланс')
async def bot_echo(message: types.Message):
    id = message.from_user.id
    user = db.select_user(id=id)
    balance = user[3]

    await message.answer(text=f'Ваш баланс {balance} баллов!', reply_markup=top_up_balance)



@dp.callback_query_handler(text='buy_points')
async def skip_task(call: CallbackQuery):
    await call.answer()
    # await call.message.answer(text='Для покупки баллов обратитись к @serg4ey')

    text1 = 'Если вы не хотите выполнять задания, тогда вы можите купить баллы. 1 Балл стоит 2 рубля.'
    text2 = 'Сколько баллов вы хотите купить?'

    await call.message.answer(text=text1)
    await call.message.answer(text=text2, reply_markup=list_of_bay1)
    # d = call.message.reply_markup.inline_keyboard[0][0].callback_data

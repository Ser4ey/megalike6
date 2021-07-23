from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp, Command, Text
from aiogram.types import ContentType, CallbackQuery

from keyboards.default.main_menu import main_menu
from loader import dp, db
from utils.misc import rate_limit
from data.list_of_goods import creat_any_invoice
from time import time


@dp.callback_query_handler(Text(['b50', 'b100', 'b250', 'b500', 'b1000', 'b2000']))
async def skip_task(call: CallbackQuery):
    await call.answer()

    cost1 = str(call.data[1:])
    # print(cost1)
    # print(call.message.chat.id)
    payload = str(call.message.chat.id) + ':' + cost1

    bxxx = creat_any_invoice(cost1)
    print(bxxx)

    await dp.bot.send_invoice(chat_id=call.message.chat.id, **bxxx, payload=payload)




@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await dp.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)



@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message):
    print('successful_payment:')
    pmnt = message.successful_payment.to_python()

    value_of_bay = 'id:777'
    for key, val in pmnt.items():
        print(f'{key} = {val}')
        if key == 'invoice_payload':
            value_of_bay = val


    user_id = int(message.chat.id)

    value_of_bay = int(value_of_bay.split(':')[-1])

    db.update_user_balance_with_const(id=user_id, change_to=value_of_bay)

    await message.answer(text=f'Вы успешно купили {value_of_bay} баллов!')
    user_balance = db.select_user(id=user_id)[3]
    await message.answer(text=f'Ваш баланс {user_balance} баллов!')
    await message.answer(text='Спасибо за покупку!', reply_markup=main_menu)


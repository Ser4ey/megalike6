from aiogram import types
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ReplyKeyboardRemove
from keyboards.default import menu
from loader import dp, db_gen_id


@dp.message_handler(Command("menu"))
async def show_menu(message: types.Message):
    await message.answer(text='menu', reply_markup=menu)


@dp.message_handler(text='1 ctroka')
async def show_menu(message: types.Message):
    await message.answer(text='AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')


@dp.message_handler(text='11')
async def show_menu(message: types.Message):
    id = db_gen_id.gen_id()
    await message.answer(text=id)


@dp.message_handler(Text(equals=['2 ctroka', '2.1 ctroka']))
async def close_menu(message: types.Message):
    await message.answer(text='OOOOOOOOOOOOOOOOOOOOOOOOO', reply_markup=ReplyKeyboardRemove())

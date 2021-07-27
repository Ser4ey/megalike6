from aiogram import types
from loader import dp
from time import sleep


@dp.message_handler()
async def bot_echo(message: types.Message):
    text = message.text
    id = message.from_user.id
    await message.answer(f'Ваш id: {id}')



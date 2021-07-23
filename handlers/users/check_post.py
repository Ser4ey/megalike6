from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp, db_active_tasks
from time import sleep
from selenium import webdriver
import asyncio


@dp.message_handler(text='2')
async def bot_echo(message: types.Message):
    a = db_active_tasks.select_all_active_tasks()
    for i in a:
        task = i
        text = f'баланс {task[2]}\nлимит {task[4]}\n src={task[1]}\nusers {task[3]}'

        await message.answer(text=text)


'''

@dp.message_handler()
async def bot_echo(message: types.Message):
    text = message.text
    if text[0] != '@':
        await message.answer(text)
        return

    await message.answer('Start ...')
    users = await Inst1.find_liked_users("https://www.instagram.com/p/CIIk4QyhOFP/")


    if users is None:
        print('sed ------------------------------------')
        await message.answer('ops')
        return
    for i in users:
        await message.answer(i)
        await asyncio.sleep(0.3)
    print(users, '333333333333333333333333333333')

'''
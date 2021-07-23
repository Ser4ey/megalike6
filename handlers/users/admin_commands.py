from aiogram import types, Dispatcher, Bot
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from loader import dp, db, db_tasks, db_active_tasks, db_gen_id, Parsing_Posts, User_and_Exists
from keyboards.default import main_menu
from states.test import Test
import time
from threading import Timer
import asyncio
from states.doing_task import DoTask
from keyboards.inline.under_task import under_task
from utils.PaseR.inst_parser import find_best, wait_your_turn



@dp.message_handler(text='1!!')
async def get_task(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text=message.from_user.id)
    if message.from_user.id == '409524113' or str(message.from_user.id) == '409524113':
        await Test.Q3.set()


@dp.message_handler(state=Test.Q3)
async def get_task(message: types.Message, state: FSMContext):
    await state.finish()

    command = message.text

    if command == '1':
        await message.answer(text=User_and_Exists)
        await message.answer(text=Parsing_Posts)
        await message.answer(text=User_and_Exists[0].queue)
        await message.answer(text=Parsing_Posts[0].queue)






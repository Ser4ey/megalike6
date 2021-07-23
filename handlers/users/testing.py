from aiogram import types
from loader import dp, Parsing_Posts, db, User_and_Exists
from utils.PaseR.inst_parser import wait_your_turn, find_best
from aiogram.dispatcher.filters import Command
from states.test import Test
from aiogram.dispatcher.storage import FSMContext

'''
@dp.message_handler(Command('test'))
async def enter_test(message: types.Message):

    await message.answer('Вы начали теcт, введите url')

    await Parsing_Posts[0].parse_user('oleg')
    await User_and_Exists[0].parse_user('natalia')



@dp.message_handler(state=Test.Q1)
async def enter1(message: types.Message, state: FSMContext):
    await state.finish()
    user = message.from_user.id

    a = db.select_user(id=user)
    await message.answer(text=a)

    # print(Parsing_Posts)
    # print(Parsing_Posts[0])
    # print(Parsing_Posts[0].queue)
   
   
    parser = find_best(Parsing_Posts)

    print(parser)


    parser = find_best(Parsing_Posts)
    u = len(parser.queue)

    await message.answer(f'Вы начали теcт, ваше место в очереди {u}')

    await wait_your_turn(parser)

    await message.answer(text='Начинаем проверку!')

    try:
        like = await parser.is_post_exist(user)
        parser.queue = parser.queue[1:]
    except:
        await message.answer(text='Не корректная ссылка!')
        parser.queue = parser.queue[1:]
        return


    if like is None:
        await message.answer(text='Такого usera net')
        return

    await message.answer(text=like)



#
    parser = find_best(Parsing_Posts)
    u = len(parser.queue)

    await message.answer(f'Вы начали теcт, ваше место в очереди {u}')

    await wait_your_turn(parser)

    await message.answer(text='Начинаем проверку!')

    try:
        like = await parser.find_liked_users(user)
        parser.queue = parser.queue[1:]
    except:
        await message.answer(text='Не корректная ссылка!')
        parser.queue = parser.queue[1:]
        return


    if like is None:
        await message.answer(text='Такого usera net')
        return

    await message.answer(text=like)
    '''
# @dp.message_handler(state=Test.Q1)
# async def answer11(message: types.Message, state: FSMContext):
#
#     answer = message.text
#     await state.update_data(answer1=answer)
#     await message.answer('Вопрос2: Sky or Fine?')
#
#     await Test.Q2.set()
#
#
# @dp.message_handler(state=Test.Q2)
# async def answer22(message: types.Message, state: FSMContext):
#     answer2 = message.text
#     data = await state.get_data()
#     answer1 = data.get('answer1')
#
#     await message.answer('Спасибо за ваши ответы')
#     await message.answer(f'Ответ 1: {answer1}')
#     await message.answer(f'Ответ 2: {answer2}')
#
#     await state.reset_state()

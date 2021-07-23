from aiogram.dispatcher.filters.state import StatesGroup, State

class DoTask(StatesGroup):
    do1 = State()
    checking_right_now = State()


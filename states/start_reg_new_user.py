from aiogram.dispatcher.filters.state import StatesGroup, State

class Start_new_user_reg(StatesGroup):
    st1 = State()
    st2 = State()
    st3 = State()
    confirm_account = State()
    problem_fix = State()

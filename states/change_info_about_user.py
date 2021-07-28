from aiogram.dispatcher.filters.state import StatesGroup, State


class ChangeInfoAboutUser(StatesGroup):
    choose_user = State()
    choose_thing_to_change = State()
    choose_value_to_change = State()



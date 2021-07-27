from aiogram.dispatcher.filters.state import StatesGroup, State


class ChangeInfoAboutUser(StatesGroup):
    choose_user = State()



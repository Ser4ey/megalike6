from aiogram.dispatcher.filters.state import StatesGroup, State


class DeleteUserByAdmin(StatesGroup):
    choose_user = State()



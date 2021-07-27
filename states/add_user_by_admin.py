from aiogram.dispatcher.filters.state import StatesGroup, State


class AddUserByAdmin(StatesGroup):
    state_id = State()
    state_instagram_name = State()
    state_phone_number = State()



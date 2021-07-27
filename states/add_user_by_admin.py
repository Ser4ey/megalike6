from aiogram.dispatcher.filters.state import StatesGroup, State
# import datetime
# print(datetime.datetime.today())


class AddUserByAdmin(StatesGroup):
    state_id = State()
    state_instagram_name = State()
    state_phone_number = State()



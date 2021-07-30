from aiogram.dispatcher.filters.state import StatesGroup, State


class DailyCheck(StatesGroup):
    send_big_text = State()
    info_by_users = State()



from aiogram.dispatcher.filters.state import StatesGroup, State


class AddTaskByUser(StatesGroup):
    task_link = State()
    description = State()
    state_phone_number = State()



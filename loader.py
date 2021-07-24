from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config

from utils.DataBase_api.sqlite_All_Users2 import DatabaseAllActiveUsers, DatabaseOfHistoryOfUsers
from utils.DataBase_api.sqlite_All_Tasks2 import DatabaseOfDayTasks



bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

db_of_active_users = DatabaseAllActiveUsers()
db_of_history_users = DatabaseOfHistoryOfUsers
db_of_dayly_tasks = DatabaseOfDayTasks()


# dp.loop.run_until_complete(bot.send_massage())



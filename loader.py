from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from utils.DataBase_api.sqllite import Database
from utils.DataBase_api.sqlite_gen_id import DatabaseGenId
from utils.DataBase_api.sqlite_tasks import DatabaseTasks
from utils.DataBase_api.sqlite_active_tasks import DatabaseActiveTasks
from utils.DataBase_api.instagram_parsers_accounts import Accounts
from utils.PaseR.inst_parser import Parse_Insta, login
from utils.PaseR.not_async_parser import Parse_Insta_Static
from selenium import webdriver
from data.config import accounts, no_accounts_comments, user_agents
# from seleniumwire import webdriver
from time import sleep
import pickle


bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database()
db_gen_id = DatabaseGenId()
db_tasks = DatabaseTasks()
db_active_tasks = DatabaseActiveTasks()
# db_parser = Accounts()

# dp.loop.run_until_complete(bot.send_massage())



# Добавление аккаунтов в таблицу
# loop = asyncio.get_event_loop()
# task = [loop.create_task(log_in_accounts(accounts, webdriver, Parse_Insta))]
# wait_task = asyncio.wait(task)
# A, B = loop.run_until_complete(wait_task)
# loop.close()
# print(A, B)
# парсинг с инстаграмы

# ubuntu server

# opt = webdriver.FirefoxOptions()
# opt.add_argument('--headless')
# web = webdriver.Firefox(executable_path='/home/ubuntu/bots_Telegram/T_bot/browser_drivers/linux/geckodriver', firefox_options=opt)
#
path_to_driwer_linux = r'browser_drivers/linux/geckodriver'
path_to_driwer_windows = r'browser_drivers/win/firefox/geckodriver.exe'
# Windows

Parsing_Posts = []
User_and_Exists = []
Parse_Comments = []

print(accounts)
for account in accounts:
    proxy = account[2]
    username = account[0]
    password = account[1]
    type1 = account[3]
    user_agent = account[4]

    firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
    firefox_capabilities['marionette'] = True

    firefox_capabilities['proxy'] = {
        "proxyType": "MANUAL",
        "httpProxy": proxy,
        "ftpProxy": proxy,
        "sslProxy": proxy
    }

    options = webdriver.FirefoxOptions()
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference("dom.webnotifications.enabled", False)
    options.set_preference("general.useragent.override", user_agent)
    options.add_argument('--headless')

    # web1 = webdriver.Firefox(capabilities=firefox_capabilities,
    #                         executable_path=path_to_driwer_windows,
    #                         firefox_binary=r"C:\Program Files\Mozilla Firefox\firefox.exe",
    #                         proxy=proxy,
    #                         options=options)



    web1 = webdriver.Firefox(capabilities=firefox_capabilities,
                             executable_path=path_to_driwer_linux,
                             proxy=proxy,
                             options=options)



    file_name = str(username) + '_cooke'
    file_path = 'data/cookies/' + file_name
    sleep(3.1)

    web1.get('https://www.instagram.com/')
    sleep(2.1)


    for cookie in pickle.load(open(file_path, 'rb')):
        web1.add_cookie(cookie)

    sleep(2)
    web1.refresh()
    sleep(3)

    # login(username, password, web1)

    Inst1 = Parse_Insta(web1, username)



    if type1 == 'parse':
        Parsing_Posts.append(Inst1)

        print(f'Аккаунт {username} успешно зарегистрирован в Parsing_Posts')
    else:
        User_and_Exists.append(Inst1)
        print(f'Аккаунт {username} успешно зарегистрирован в User_and_Exists')

    Inst = 0
    u1 = 0
    web = 0

'''
for account1 in no_accounts_comments:
    name = no_accounts_comments[0]
    print(name)

    firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
    firefox_capabilities['marionette'] = True

    options = webdriver.FirefoxOptions()
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference("dom.webnotifications.enabled", False)
    options.set_preference("general.useragent.override", user_agents[0])
    options.add_argument('--headless')

    web1 = webdriver.Firefox(capabilities=firefox_capabilities,
                             executable_path=path_to_driwer_windows,
                             firefox_binary=r"C:\Program Files\Mozilla Firefox\firefox.exe",
                             options=options
                             )

    src1 = 'https://www.instagram.com/p/CKwoVAOLrzV/?igshid=1q4sb72f4tgql'


    WebD = Parse_Insta(web1, name)


    Parse_Comments.append(WebD)

    print('Аккаунт', name, 'арегистрирован ParseComment')

'''
print(Parsing_Posts, User_and_Exists, Parse_Comments)


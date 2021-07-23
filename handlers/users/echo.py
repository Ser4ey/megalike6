from aiogram import types
from loader import dp, db_active_tasks
from time import sleep


from time import sleep
from selenium import webdriver
import numpy as np
from selenium.webdriver.support import expected_conditions as EC
import copy
import csv
import datetime
import asyncio


class Parse_Insta:

    def __init__(self, driver):
        self.web = driver

    async def wait_until_cond(self, css):
        flag = 0
        while True:
            try:
                self.web.find_element_by_css_selector(css)
                break
            except Exception:
                if (flag < 20):
                    await asyncio.sleep(0.3)
                    flag += 1
                else:
                    raise Exception("TimeLimit")

    async def find_liked_users(self, url):
        self.web.switch_to.window(self.web.current_window_handle)
        self.web.get(url)
        await asyncio.sleep(1)
        await self.wait_until_cond("button.sqdOP.yWX7d._8A5w5")
        await asyncio.sleep(1)
        self.web.find_elements_by_css_selector("button.sqdOP.yWX7d._8A5w5")[-1].click()
        while len(self.web.find_elements_by_css_selector("a.FPmhX.notranslate.MBL3Z")) == 0:
            await asyncio.sleep(1)
        await asyncio.sleep(0.5)
        users = set([])
        max_len = -1
        cnt = 0
        while max_len < len(users) or cnt < 3:
            if max_len == len(users):
                cnt += 1
            else:
                cnt = 0
            max_len = len(users)
            new_users = set()
            for user in self.web.find_elements_by_css_selector("a.FPmhX.notranslate.MBL3Z"):
                new_users.add(user.text)
            users = users | new_users
            last = self.web.find_elements_by_css_selector("a.FPmhX.notranslate.MBL3Z")[-2]
            last.location_once_scrolled_into_view
            await asyncio.sleep(0.2)
            last = self.web.find_elements_by_css_selector("a.FPmhX.notranslate.MBL3Z")[3]
            last.location_once_scrolled_into_view
            await asyncio.sleep(1)
        return list(users)

    async def find_comments(self, url):
        self.web.switch_to.window(self.web.current_window_handle)
        data = {}
        cnt = 0
        self.web.get(url)
        await asyncio.sleep(2)
        try:
            await self.wait_until_cond("span.glyphsSpriteCircle_add__outline__24__grey_9.u-__7")
        except Exception:
            pass
        while self.web.find_elements_by_css_selector(
                "span.glyphsSpriteCircle_add__outline__24__grey_9.u-__7") != [] or cnt < 2:
            for elem in self.web.find_elements_by_css_selector("div.C4VMK")[1:]:
                user = elem.text.split("\n")[0]
                text = elem.text.split("\n")[1]
                if (user not in data):
                    data[user] = text
                else:
                    if text not in data[user]:
                        data[user] += (";" + text)
            await asyncio.sleep(0.5)
            last = self.web.find_elements_by_css_selector("div.C4VMK")[-2]
            await last.location_once_scrolled_into_view
            await asyncio.sleep(1)
            if self.web.find_elements_by_css_selector("span.glyphsSpriteCircle_add__outline__24__grey_9.u-__7") == []:
                cnt += 1
                await asyncio.sleep(1)
            else:
                self.web.find_element_by_css_selector("span.glyphsSpriteCircle_add__outline__24__grey_9.u-__7").click()
                cnt = 0
        return data

    async def find_users_who_comment(self, url):
        self.web.switch_to.window(self.web.current_window_handle)
        data = {}
        cnt = 0
        users = set()
        self.web.get(url)
        await asyncio.sleep(1)
        try:
            await self.wait_until_cond("span.glyphsSpriteCircle_add__outline__24__grey_9.u-__7")
        except Exception:
            pass
        while self.web.find_elements_by_css_selector(
                "span.glyphsSpriteCircle_add__outline__24__grey_9.u-__7") != [] or cnt < 2:
            for elem in self.web.find_elements_by_css_selector("div.C4VMK")[1:]:
                user = elem.text.split("\n")[0]
                users.add(user)
            await asyncio.sleep(0.5)
            last = self.web.find_elements_by_css_selector("div.C4VMK")[-2]
            await last.location_once_scrolled_into_view
            await asyncio.sleep(1)
            if self.web.find_elements_by_css_selector("span.glyphsSpriteCircle_add__outline__24__grey_9.u-__7") == []:
                cnt += 1
                await asyncio.sleep(1)
            else:
                self.web.find_element_by_css_selector("span.glyphsSpriteCircle_add__outline__24__grey_9.u-__7").click()
                cnt = 0
        return list(users)

    async def parse_user(self, username):
        self.web.switch_to.window(self.web.current_window_handle)
        self.web.get("https://www.instagram.com/")
        await asyncio.sleep(1)
        await self.wait_until_cond("div.eyXLr.wUAXj")
        self.web.find_element_by_css_selector("div.eyXLr.wUAXj").click()
        await asyncio.sleep(0.5)
        self.web.find_element_by_css_selector("input.XTCLo.x3qfX").send_keys(username)
        sleep(2)
        self.web.find_element_by_css_selector("span.Ap253").click()
        await asyncio.sleep(2)
        await self.wait_until_cond("span.g47SY")
        await asyncio.sleep(1)
        stats = self.web.find_elements_by_css_selector("span.g47SY")
        data = dict()
        data["Постов"] = stats[0].text
        data["Подписчиков"] = stats[1].text
        data["Подписок"] = stats[2].text
        return data






@dp.message_handler(text='2')
async def bot_echo(message: types.Message):
    a = db_active_tasks.select_all_active_tasks()
    for i in a:
        await message.answer(i)

    #     переслать сообщение



@dp.message_handler()
async def bot_echo(message: types.Message):
    # web = webdriver.Chrome("C:\\Users\\днс\\Downloads\\chromedriver.exe")
    # web.get("https://www.instagram.com/")
    # await asyncio.sleep(35)
    # await message.reply('users')
    # Inst = Parse_Insta(web)
    #
    # users = await Inst.find_liked_users("https://www.instagram.com/p/CIN_dvFn4o7/")
    # print(users)
    # await message.answer(text = f'{users}')
    # await asyncio.sleep(5)
    # await message.reply('users')

    text = message.text
    if text[0] != '@':
        await message.answer(text)
        return


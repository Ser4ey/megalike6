from selenium import webdriver
import numpy as np
from selenium.webdriver.support import expected_conditions as EC
import copy
import csv
import datetime
import asyncio
from time import time, sleep

class Parse_Insta:
    def __init__(self, driver, account_name):
        self.web = driver
        self.account_name = account_name
        self.queue = []

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

    async def find_liked_users(self, url):  ## CHECKED
        self.web.switch_to.window(self.web.current_window_handle)
        self.web.get(url)
        await asyncio.sleep(1)
        try:
            self.web.find_element_by_css_selector("button.aOOlW.HoLwm").click()
        except Exception:
            pass
        if len(self.web.find_elements_by_css_selector("button.sqdOP.yWX7d._8A5w5")) == 0:
            print('no parse like')
            return None
        # correct
        await self.wait_until_cond("button.sqdOP.yWX7d._8A5w5")
        # correct
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

            last = self.web.find_elements_by_css_selector("a.FPmhX.notranslate.MBL3Z")[-1]
            last.location_once_scrolled_into_view
            await asyncio.sleep(0.2)
            last = self.web.find_elements_by_css_selector("a.FPmhX.notranslate.MBL3Z")[1]
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
            self.web.find_element_by_css_selector("button.aOOlW.HoLwm").click()
        except Exception:
            pass
        if len(self.web.find_elements_by_css_selector("button.sqdOP.yWX7d._8A5w5")) == 0:
            return None
        try:
            #
            await self.wait_until_cond("span.glyphsSpriteCircle_add__outline__24__grey_9.u-__7")
        except Exception:
            pass
        while cnt < 2:
            for elem in self.web.find_elements_by_css_selector("div.C4VMK")[1:]:
                user = elem.text.split("\n")[0]
                text = elem.text.split("\n")[1]
                if (user not in data):
                    data[user] = text
                else:
                    if text not in data[user]:
                        data[user] += (";" + text)
            await asyncio.sleep(0.5)
            last = self.web.find_elements_by_css_selector("div.C4VMK")[-1]
            last.location_once_scrolled_into_view
            last = self.web.find_elements_by_css_selector("div.C4VMK")[0]
            last.location_once_scrolled_into_view
            last = self.web.find_elements_by_css_selector("div.C4VMK")[0]
            last.location_once_scrolled_into_view
            await asyncio.sleep(1)
            try:
                self.web.find_element_by_css_selector("span.glyphsSpriteCircle_add__outline__24__grey_9.u-__7").click()
                cnt = 0
            except Exception:
                cnt += 1
        return data

    async def find_users_who_comment(self, url):
        self.web.switch_to.window(self.web.current_window_handle)
        data = {}
        cnt = 0
        users = set()
        self.web.get(url)
        await asyncio.sleep(1)
        try:
            self.web.find_element_by_css_selector("button.aOOlW.HoLwm").click()
        except Exception:
            pass
        if len(self.web.find_elements_by_css_selector("button.sqdOP.yWX7d._8A5w5")) == 0:
            return None
        try:
            #
            await self.wait_until_cond("span.glyphsSpriteCircle_add__outline__24__grey_9.u-__7")
        except Exception:
            pass
        while cnt < 2:
            for elem in self.web.find_elements_by_css_selector("div.C4VMK")[1:]:
                user = elem.text.split("\n")[0]
                users.add(user)
            await asyncio.sleep(0.5)
            last = self.web.find_elements_by_css_selector("div.C4VMK")[-1]
            last.location_once_scrolled_into_view
            last = self.web.find_elements_by_css_selector("div.C4VMK")[0]
            last.location_once_scrolled_into_view
            last = self.web.find_elements_by_css_selector("div.C4VMK")[0]
            last.location_once_scrolled_into_view
            await asyncio.sleep(1)
            try:
                self.web.find_element_by_css_selector("span.glyphsSpriteCircle_add__outline__24__grey_9.u-__7").click()
                cnt = 0
            except Exception:
                cnt += 1
        return list(users)

    async def parse_user(self, username):
        self.web.switch_to.window(self.web.current_window_handle)
        self.web.get("https://www.instagram.com/")
        await asyncio.sleep(2)
        try:
            self.web.find_element_by_css_selector("button.aOOlW.HoLwm").click()
        except Exception:
            pass
        #
        await self.wait_until_cond("div.eyXLr.wUAXj")
        self.web.find_element_by_css_selector("div.eyXLr.wUAXj").click()
        await asyncio.sleep(0.5)
        self.web.find_element_by_css_selector("input.XTCLo.x3qfX").send_keys(username)
        await asyncio.sleep(2)
        if len(self.web.find_elements_by_css_selector("span.Ap253")) == 0:
            return None
        try:
            self.web.find_element_by_css_selector("span.Ap253").click()
            await asyncio.sleep(2)
            #
            await self.wait_until_cond("span.g47SY")
            await asyncio.sleep(1)
            stats = self.web.find_elements_by_css_selector("span.g47SY")
            data = dict()
            data["Постов"] = stats[0].text
            data["Подписчиков"] = stats[1].text
            data["Подписок"] = stats[2].text
            return data
        except Exception:
            return None



    async def parse_user_without_search(self, username):
        self.web.get(f"https://www.instagram.com/{username}/")
        await asyncio.sleep(1)

        try:
            await asyncio.sleep(1)
            #
            await self.wait_until_cond("span.g47SY")
            await asyncio.sleep(1)
            stats = self.web.find_elements_by_css_selector("span.g47SY")
            data = dict()
            data["Постов"] = stats[0].text
            data["Подписчиков"] = stats[1].text
            data["Подписок"] = stats[2].text
            return data
        except Exception:
            return None



    async def find_comments_fromS(self, url):
        try:
            self.web.switch_to.window(self.web.current_window_handle)
            data = {}
            cnt = 0
            time_counter = 0
            self.web.get(url)
            await asyncio.sleep(2)
            try:
                self.web.find_element_by_css_selector("button.aOOlW.HoLwm").click()
            except Exception:
                pass
            if len(self.web.find_elements_by_css_selector("button.sqdOP.yWX7d._8A5w5")) == 0:
                return None
            try:
                #
                await self.wait_until_cond("span.glyphsSpriteCircle_add__outline__24__grey_9.u-__7")
            except Exception:
                pass
            while cnt < 2 and time_counter < 5:
                for elem in self.web.find_elements_by_css_selector("div.C4VMK")[1:]:
                    user = elem.text.split("\n")[0]
                    text = elem.text.split("\n")[1]
                    if (user not in data):
                        data[user] = text
                    else:
                        if text not in data[user]:
                            data[user] += (";" + text)
                await asyncio.sleep(0.5)
                last = self.web.find_elements_by_css_selector("div.C4VMK")[-1]
                last.location_once_scrolled_into_view
                last = self.web.find_elements_by_css_selector("div.C4VMK")[0]
                last.location_once_scrolled_into_view
                last = self.web.find_elements_by_css_selector("div.C4VMK")[0]
                last.location_once_scrolled_into_view
                await asyncio.sleep(1)
                try:
                    self.web.find_element_by_css_selector("span.glyphsSpriteCircle_add__outline__24__grey_9.u-__7").click()
                    time_counter += 1
                    cnt = 0
                except Exception:
                    time_counter += 1
                    cnt += 1
        except:
            data = {'tl': 'True'}
            return data

        if time_counter < 5:
            return data
        else:
            data['tl'] = 'True'
            return data


    #
    async def is_post_exist(self, url):  ## CHECKED
        self.web.switch_to.window(self.web.current_window_handle)
        self.web.get(url)
        await asyncio.sleep(1)

        try:
            self.web.find_element_by_css_selector("button.aOOlW.HoLwm").click()
        except Exception:
            pass
        if len(self.web.find_elements_by_css_selector("button.sqdOP.yWX7d._8A5w5")) == 0:
            return None
        # correct
        return True





    async def find_liked_users_from_olegS(self, url):  ## CHECKED
        try:
            self.web.switch_to.window(self.web.current_window_handle)
            self.web.get(url)
            await asyncio.sleep(1)
            try:
                self.web.find_element_by_css_selector("button.aOOlW.HoLwm").click()
            except Exception:
                pass
            if len(self.web.find_elements_by_css_selector("button.sqdOP.yWX7d._8A5w5")) == 0:
                print('no parse like')
                return None
            # correct
            await self.wait_until_cond("button.sqdOP.yWX7d._8A5w5")
            # correct
            await asyncio.sleep(1)
            try:
                self.web.find_elements_by_css_selector("button.sqdOP.yWX7d._8A5w5")[-1].click()
                while len(self.web.find_elements_by_css_selector("a.FPmhX.notranslate.MBL3Z")) == 0:
                    await asyncio.sleep(1)

            except:
                pass

            await asyncio.sleep(0.5)
            users = set([])
            max_len = -1
            cnt = 0
            while max_len < len(users) or cnt < 3:
                if max_len == len(users):
                    cnt += 1
                else:
                    cnt += 1
                max_len = len(users)
                new_users = set()
                for user in self.web.find_elements_by_css_selector("a.FPmhX.notranslate.MBL3Z"):
                    new_users.add(user.text)

                users = users | new_users

                try:
                    last = self.web.find_elements_by_css_selector("a.FPmhX.notranslate.MBL3Z")[-1]
                    last.location_once_scrolled_into_view
                    await asyncio.sleep(0.2)
                    last = self.web.find_elements_by_css_selector("a.FPmhX.notranslate.MBL3Z")[1]
                    last.location_once_scrolled_into_view
                    await asyncio.sleep(1)
                except:
                    cnt += 1

            return list(users)
        except:
            print('Ошибка при парсенге лайков')
            return 'error123'

    #

    async def find_comments_best_last_S(self, url):
        self.web.switch_to.window(self.web.current_window_handle)
        data = {}
        cnt = 0
        self.web.get(url)
        await asyncio.sleep(2)
        try:
            self.web.find_element_by_css_selector("button.aOOlW.HoLwm").click()
        except Exception:
            pass
        if len(self.web.find_elements_by_css_selector("button.sqdOP.yWX7d._8A5w5")) == 0:
            return None
        try:
            #
            await self.wait_until_cond("span.glyphsSpriteCircle_add__outline__24__grey_9.u-__7")
        except Exception:
            pass
        while cnt < 3:
            for elem in self.web.find_elements_by_css_selector("div.C4VMK")[1:]:
                user = elem.text.split("\n")[0]
                text = elem.text.split("\n")[1]
                if (user not in data):
                    data[user] = text
                else:
                    if text not in data[user]:
                        data[user] += (";" + text)
            await asyncio.sleep(0.5)
            last = self.web.find_elements_by_css_selector("div.C4VMK")[-1]
            last.location_once_scrolled_into_view
            last = self.web.find_elements_by_css_selector("div.C4VMK")[0]
            last.location_once_scrolled_into_view
            last = self.web.find_elements_by_css_selector("div.C4VMK")[0]
            last.location_once_scrolled_into_view
            await asyncio.sleep(1)
            # try:
            #     self.web.find_element_by_css_selector("span.glyphsSpriteCircle_add__outline__24__grey_9.u-__7").click()
            #     cnt = 0
            # except Exception:
            #     cnt += 1
            cnt += 1
        return data





    def quit(self):
        self.web.close()
        self.web.quit()



def login(username, password, web):
    sleep(1)
    web.get("https://www.instagram.com/")
    sleep(3)
    web.find_elements_by_css_selector("input._2hvTZ.pexuQ.zyHYP")[0].send_keys(username)
    sleep(1.2)
    web.find_elements_by_css_selector("input._2hvTZ.pexuQ.zyHYP")[1].send_keys(password)
    sleep(1)
    web.find_element_by_css_selector("button.sqdOP.L3NKy.y3zKF").click()


async def wait_your_turn(Inst):
    # добавление задачи в очередь
    while True:
        time_id = time()
        if time_id in Inst.queue:
            continue
        else:
            Inst.queue.append(time_id)
            break


    # ожидание очереди
    while True:
        print('work...', time_id)
        if len(Inst.queue) == 0:
            break


        if Inst.queue[0] == time_id:
            print(f'Time {time_id}')
            break

        await asyncio.sleep(3)


def find_best(List_of_accounts):
    if len(List_of_accounts) == 0:
        return None

    min_value = len(List_of_accounts[0].queue)
    best_index = 0
    for i in range(len(List_of_accounts)):
        acc = List_of_accounts[i]
        if min_value > len(acc.queue):
            min_value = len(acc.queue)
            best_index = i

    return List_of_accounts[best_index]



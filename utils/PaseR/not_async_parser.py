from time import sleep

class Parse_Insta_Static:


    def __init__(self, driver):
        self.web = driver

    def wait_until_cond(self, css):
        flag = 0
        while True:
            try:
                self.web.find_element_by_css_selector(css)
                break
            except Exception:
                if (flag < 20):
                    sleep(0.3)
                    flag += 1
                else:
                    raise Exception("TimeLimit")

    def find_liked_users(self, url):  ## CHECKED
        self.web.switch_to.window(self.web.current_window_handle)
        self.web.get(url)
        sleep(1)
        try:
            self.web.find_element_by_css_selector("button.aOOlW.HoLwm").click()
        except Exception:
            pass
        if len(self.web.find_elements_by_css_selector("button.sqdOP.yWX7d._8A5w5")) == 0:
            return None
        self.wait_until_cond("button.sqdOP.yWX7d._8A5w5")
        sleep(1)
        self.web.find_elements_by_css_selector("button.sqdOP.yWX7d._8A5w5")[-1].click()
        while len(self.web.find_elements_by_css_selector("a.FPmhX.notranslate.MBL3Z")) == 0:
            sleep(1)
        sleep(0.5)
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
            sleep(0.2)
            last = self.web.find_elements_by_css_selector("a.FPmhX.notranslate.MBL3Z")[1]
            last.location_once_scrolled_into_view
            sleep(1)
        return list(users)

    def find_comments(self, url):
        self.web.switch_to.window(self.web.current_window_handle)
        data = {}
        cnt = 0
        self.web.get(url)
        sleep(2)
        try:
            self.web.find_element_by_css_selector("button.aOOlW.HoLwm").click()
        except Exception:
            pass
        if len(self.web.find_elements_by_css_selector("button.sqdOP.yWX7d._8A5w5")) == 0:
            return None
        try:
            self.wait_until_cond("span.glyphsSpriteCircle_add__outline__24__grey_9.u-__7")
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
            sleep(0.5)
            last = self.web.find_elements_by_css_selector("div.C4VMK")[-1]
            last.location_once_scrolled_into_view
            last = self.web.find_elements_by_css_selector("div.C4VMK")[0]
            last.location_once_scrolled_into_view
            last = self.web.find_elements_by_css_selector("div.C4VMK")[0]
            last.location_once_scrolled_into_view
            sleep(1)
            try:
                self.web.find_element_by_css_selector("span.glyphsSpriteCircle_add__outline__24__grey_9.u-__7").click()
                cnt = 0
            except Exception:
                cnt += 1
        return data

    def find_users_who_comment(self, url):
        self.web.switch_to.window(self.web.current_window_handle)
        data = {}
        cnt = 0
        users = set()
        self.web.get(url)
        sleep(1)
        try:
            self.web.find_element_by_css_selector("button.aOOlW.HoLwm").click()
        except Exception:
            pass
        if len(self.web.find_elements_by_css_selector("button.sqdOP.yWX7d._8A5w5")) == 0:
            return None
        try:
            self.wait_until_cond("span.glyphsSpriteCircle_add__outline__24__grey_9.u-__7")
        except Exception:
            pass
        while cnt < 2:
            for elem in self.web.find_elements_by_css_selector("div.C4VMK")[1:]:
                user = elem.text.split("\n")[0]
                users.add(user)
            sleep(0.5)
            last = self.web.find_elements_by_css_selector("div.C4VMK")[-1]
            last.location_once_scrolled_into_view
            last = self.web.find_elements_by_css_selector("div.C4VMK")[0]
            last.location_once_scrolled_into_view
            last = self.web.find_elements_by_css_selector("div.C4VMK")[0]
            last.location_once_scrolled_into_view
            sleep(1)
            try:
                self.web.find_element_by_css_selector("span.glyphsSpriteCircle_add__outline__24__grey_9.u-__7").click()
                cnt = 0
            except Exception:
                cnt += 1
        return list(users)

    def parse_user(self, username):
        self.web.switch_to.window(self.web.current_window_handle)
        self.web.get("https://www.instagram.com/")
        sleep(2)
        try:
            self.web.find_element_by_css_selector("button.aOOlW.HoLwm").click()
        except Exception:
            pass
        self.wait_until_cond("div.eyXLr.wUAXj")
        self.web.find_element_by_css_selector("div.eyXLr.wUAXj").click()
        sleep(0.5)
        self.web.find_element_by_css_selector("input.XTCLo.x3qfX").send_keys(username)
        sleep(2)
        if len(self.web.find_elements_by_css_selector("span.Ap253")) == 0:
            return None
        try:
            self.web.find_element_by_css_selector("span.Ap253").click()
            sleep(2)
            self.wait_until_cond("span.g47SY")
            sleep(1)
            stats = self.web.find_elements_by_css_selector("span.g47SY")
            data = dict()
            data["Постов"] = stats[0].text
            data["Подписчиков"] = stats[1].text
            data["Подписок"] = stats[2].text
            return data
        except Exception:
            return None

    def login(self, username, password):
        sleep(1)
        self.web.get("https://www.instagram.com/")
        sleep(3.3)
        self.web.find_elements_by_css_selector("input._2hvTZ.pexuQ.zyHYP")[0].send_keys(username)
        sleep(1.2)
        self.web.find_elements_by_css_selector("input._2hvTZ.pexuQ.zyHYP")[1].send_keys(password)
        sleep(1.1)
        self.web.find_element_by_css_selector("button.sqdOP.L3NKy.y3zKF").click()



    def find_comments20(self, url):
        self.web.switch_to.window(self.web.current_window_handle)
        data = {}
        cnt = 0
        self.web.get(url)
        sleep(2)
        try:
            self.web.find_element_by_css_selector("button.aOOlW.HoLwm").click()
        except Exception:
            pass
        if len(self.web.find_elements_by_css_selector("button.sqdOP.yWX7d._8A5w5")) == 0:
            return None
        try:
            self.wait_until_cond("span.glyphsSpriteCircle_add__outline__24__grey_9.u-__7")
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
            sleep(0.5)
            last = self.web.find_elements_by_css_selector("div.C4VMK")[-1]
            last.location_once_scrolled_into_view
            last = self.web.find_elements_by_css_selector("div.C4VMK")[0]
            last.location_once_scrolled_into_view
            last = self.web.find_elements_by_css_selector("div.C4VMK")[0]
            last.location_once_scrolled_into_view
            sleep(1)
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
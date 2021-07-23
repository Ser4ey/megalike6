from selenium import webdriver
from utils.PaseR.not_async_parser import Parse_Insta_Static
from data.config import accounts

try:
    account = accounts[0]

    proxy = account[2]
    username = account[0]
    password = account[1]
    type1 = account[3]
    user_agent = account[4]

    firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
    firefox_capabilities['marionette'] = True

    # firefox_capabilities['proxy'] = {
    #     "proxyType": "MANUAL",
    #     "httpProxy": proxy,
    #     "ftpProxy": proxy,
    #     "sslProxy": proxy
    # }

    options = webdriver.FirefoxOptions()
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference("dom.webnotifications.enabled", False)
    options.set_preference("general.useragent.override", user_agent)


    web1 = webdriver.Firefox(capabilities=firefox_capabilities,
                            executable_path="C:\\Users\\днс\Desktop\\bot oleg\\browser_drivers\\win\\firefox\\geckodriver",
                            firefox_binary=r"C:\Program Files\Mozilla Firefox\firefox.exe",
                            options=options)




    src1 = 'https://www.instagram.com/p/CKwoVAOLrzV/?igshid=1q4sb72f4tgql'
    src2 = 'https://www.instagram.com/p/CDybZC2B_vA/?igshid=zjaykrh9ayc5'

    WebD = Parse_Insta_Static(web1)
    print('1 state')
    result = WebD.find_comments20(src2)
    for i, b in result.items():
        print(i, b)


    WebD.quit()
except Exception as er:
    print(er)
finally:
    print('done')



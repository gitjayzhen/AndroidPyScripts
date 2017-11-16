# coding=utf-8
from appium import webdriver


class MyDriver:

    def __init__(self, port, appPackage, activityName):
        self.__port = port
        self.__baseUrl = "http://localhost:"+self.__port+"/wd/hub"
        self.__desired_caps = {
                        "platformName": "Android",
                        "platformVersion": "4.4.4",
                        "deviceName": "nox",
                        #"udid": udid,
                        "newCommandTimeout": "15",
                        "unicodeKeyboard": "True",
                        "resetKeyboard": "True",
                        "noSign": "True",
                        "appPackage": appPackage,
                        "appActivity": activityName
                }

    def driver(self):
        return webdriver.Remote(self.__baseUrl, self.__desired_caps)

nox = MyDriver("4723", "com.longtu.weifuhua", "com.longtu.weifuhua.ui.personcenter.activity.PersonalLoadingActivity")
nox1 = MyDriver("4725", "com.longtu.weifuhua", "com.longtu.weifuhua.ui.personcenter.activity.PersonalLoadingActivity")
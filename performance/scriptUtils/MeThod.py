# coding=utf-8
from selenium.webdriver.common.by import By
from DataBase import *
from MyDriver import nox


class MeThod:
    def __init__(self):
        self.__driver = nox.driver()

    @property
    def api(self):
        return self.__driver

    def findElement(self, method, id):
        if method == "xpath":
            return self.__driver.find_element(by=By.XPATH, value=db_eles.select(method, id))
        if method == "id":
            return self.__driver.find_element(by=By.ID, value=db_eles.select(method, id))
        if method == "name":
            return self.__driver.find_element(by=By.NAME, value=db_eles.select(method, id))
        if method == "calss_name":
            return self.__driver.find_element(by=By.CLASS_NAME, value=db_eles.select(method, id))
        else:
            return None

    def out(self):
        self.findElement("xpath", "1").click()
        try:
            text = self.findElement("xpath", "9").text
        except Exception:
            text = None
        phone = ""
        if text == phone:
            self.__driver.tap([(150, 235)])
            self.findElement("xpath", "2").click()
            self.findElement("xpath", "3").click()
        else:
            self.findElement("xpath", "3").click()
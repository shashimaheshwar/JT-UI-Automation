from selenium import webdriver
from ConfigVars.TestConfig import variables
from ConfigVars.FrameworkConfig import urls


class DriverIntialization():

    baseURL = urls.HOME_PAGE

    def __init__(self,baseURL):
        self.driver = webdriver.Chrome("")
        self.driver.maximize_window()
        self.driver.implicitly_wait(variables.WAIT)
        self.driver.get(baseURL)

    def return_driver(self):
        return self.driver

from UtilityPackage.SeleniumDriver import SeleniumDriver
import json

"""
PaymentClassJT: Surprise your loved ones on big screens
"""


class CheersAndGreetingsJT(SeleniumDriver):

    def __init__(self, driver, locator):
        #super().__init__(driver)
        self.driver = driver
        with open(locator) as f:
            data = json.load(f)
        self.locator = data

    def skip_cheers_greetings(self):
        self.elementClick(self.locator["skip_cheers"]["xpath"], locatorType="xpath")

    def verify_ticket_booking(self):
        element = self.isElementPresent(self.locator["skip_cheers"]["xpath"], locatorType="xpath")
        return element

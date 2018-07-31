from UtilityPackage.SeleniumDriver import SeleniumDriver
from ConfigVars import variables
import time

"""
PaymentClassJT: Surprise your loved ones on big screens
"""


class CheersAndGreetingsJT(SeleniumDriver):

    def __init__(self, driver):
        #super().__init__(driver)
        self.driver = driver

    skip_cheers="//*[contains(text(),'Skip and Proceed to View Ticket')]"

    def skip_cheers_greetings(self):
        self.elementClick(self.skip_cheers, locatorType="xpath")

    def verify_ticket_booking(self):
        element = self.isElementPresent(self.skip_cheers, locatorType="xpath")
        return element

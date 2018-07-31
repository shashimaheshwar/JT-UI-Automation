from UtilityPackage.SeleniumDriver import SeleniumDriver
from ConfigVars import variables
import time

"""
FoodAndBrevrageJT:Skip F&B or Order_fnb_item.
"""


class FoodAndBrevrageJT(SeleniumDriver):

    def __init__(self, driver):
        self.driver = driver

    skip_cheers = "//*[contains(text(),'Skip F&B and Pay')]"

    def skip_food_brev(self):
        self.elementClick(self.skip_cheers, locatorType="xpath")

    def verify_existence_fnb(self):
        element = self.isElementPresent(self.skip_cheers, locatorType="xpath")
        return element

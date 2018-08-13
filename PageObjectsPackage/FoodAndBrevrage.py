from UtilityPackage.SeleniumDriver import SeleniumDriver
from ConfigVars import variables
import json

"""
FoodAndBrevrageJT:Skip F&B or Order_fnb_item.
"""


class FoodAndBrevrageJT(SeleniumDriver):

    def __init__(self, driver, locator):
        self.driver = driver
        with open(locator) as f:
            data = json.load(f)
        self.locator = data

    def skip_food_brev(self):
        self.elementClick(self.locator["skip_cheers"]["xpath"], locatorType="xpath")

    def verify_existence_fnb(self):
        element = self.isElementPresent(self.locator["skip_cheers"]["xpath"], locatorType="xpath")
        return element

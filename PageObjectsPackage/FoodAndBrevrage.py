from UtilityPackage.SeleniumDriver import SeleniumDriver
import json, time

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

    def confirm_order(self):
        self.elementClick(self.locator["confirm_order"]["xpath"], locatorType="xpath")

    def verify_existence_fnb(self):
        element = self.isElementPresent(self.locator["skip_cheers"]["xpath"], locatorType="xpath")
        return element

    def get_fnb_items_avliable(self):
        items=[]
        element_list=self.getElements(self.locator["fnb_itemList"]["xpath"], locatorType="xpath")
        for item in element_list:
            items.append(item.text)
        return items

    def add_fnb_items(self, item,count):
        for ele in self.getElements(self.locator["food_details"]["xpath"]+self.locator["food_item"]["xpath"].format(item), locatorType="xpath"):
            if ele.text in self.get_fnb_items_avliable():
                for it in range(count):
                    time.sleep(5)
                    self.elementClick(self.locator["food_details"]["xpath"]+self.locator["increment"]["xpath"], locatorType="xpath")
            else:
                pass
from UtilityPackage.SeleniumDriver import SeleniumDriver
import json, time
import UtilityPackage.CustomLogger as cl
import logging

"""
FoodAndBrevrageJT:Skip F&B or Order_fnb_item.
"""


class FoodAndBrevrageJT(SeleniumDriver):

    def __init__(self, driver, locator):
        self.driver = driver
        with open(locator) as f:
            data = json.load(f)
        self.locator = data

    log = cl.customLogger(logging.DEBUG)

    def skip_food_brev(self):
        self.log.info("Skipping the food and beverage items")
        self.elementClick(self.locator["skip_cheers"]["xpath"], locatorType="xpath")

    def confirm_order(self):
        self.log.info("Confirming the orders")
        self.elementClick(self.locator["confirm_order"]["xpath"], locatorType="xpath")

    def verify_existence_fnb(self):
        self.log.info("Checking the existence of Food and beverage item")
        element = self.isElementPresent(self.locator["skip_cheers"]["xpath"], locatorType="xpath")
        return element

    def get_fnb_items_avliable(self):
        items=[]
        self.log.info("get fnb items avaliable ")
        element_list=self.getElements(self.locator["fnb_itemList"]["xpath"], locatorType="xpath")
        for item in element_list:
            items.append(item.text)
        self.log.info("Food and beverage list"+",".join(items))
        return items

    def add_fnb_items(self, item,count):
        self.log.info("Getting the all Food details")
        parent_elem = self.getElements(self.locator["food_details"]["xpath"], locatorType="xpath")
        for parent_element in parent_elem:
            self.log.info("Getting all  child attribute of food details")
            if parent_element.find_element_by_class_name('header').text == item:
                self.log.info("Checking particular item exist in the Item lists")
                for itr in range(count):
                    self.log.info("Adding the f&b item as per input")
                    parent_element.find_element_by_class_name('increment').click()
                    time.sleep(5)
                    self.log.info("FnB item added successfully")
            else:
                self.log.info("F&B item requested could not added as it is not available")

    def add_fnb_items_list(self, item,count):
        self.log.info("Getting the all Food details")
        parent_elem = self.getElements(self.locator["food_details"]["xpath"], locatorType="xpath")
        for parent_element in parent_elem:
            self.log.info("Getting all  child attribute of food details")
            for food_item in item:
                if parent_element.find_element_by_class_name('header').text in food_item:
                    self.log.info("Checking particular item exist in the Item lists")
                    for itr in range(count):
                        self.log.info("Adding the f&b item as per input")
                        parent_element.find_element_by_class_name('increment').click()
                        time.sleep(5)
                        self.log.info("FnB item added successfully")
                else:
                    self.log.info("F&B item requested could not added as it is not available")

    def remove_fnb_items(self, item, count):
        self.log.info("Getting the all Food details")
        parent_elem = self.getElements(self.locator["food_details"]["xpath"], locatorType="xpath")
        for parent_element in parent_elem:
            self.log.info("Getting all  child attribute of food details")
            if parent_element.find_element_by_class_name('header').text == item:
                self.log.info("Checking particular item exist in the Item lists")
                for itr in range(count):
                    self.log.info("Adding the f&b item as per input")
                    parent_element.find_element_by_class_name('decrement').click()
                    time.sleep(5)
                    self.log.info("FnB item removed successfully")
            else:
                self.log.info("F&B item requested could not removed as it is not available")

    def remove_fnb_items_list(self, item,count):
        self.log.info("Getting the all Food details")
        parent_elem = self.getElements(self.locator["food_details"]["xpath"], locatorType="xpath")
        for parent_element in parent_elem:
            self.log.info("Getting all  child attribute of food details")
            for food_item in item:
                if parent_element.find_element_by_class_name('header').text in food_item:
                    self.log.info("Checking particular item exist in the Item lists")
                    for itr in range(count):
                        self.log.info("Adding the f&b item as per input")
                        parent_element.find_element_by_class_name('decrement').click()
                        time.sleep(5)
                        self.log.info("FnB item added successfully")
                else:
                    self.log.info("F&B item requested could not added as it is not available")

    def manage_order(self):
        self.log.info("Going back to the F&B page to mange the orders")
        self.elementClick(self.locator["mange_food"]["xpath"], locatorType="xpath")

    def cancel_changes(self):
        self.log.info("Canceling the changes done, Keeping the Original F&B order ")
        self.elementClick(self.locator["cancel_changes"]["xpath"], locatorType="xpath")


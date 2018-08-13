from UtilityPackage.SeleniumDriver import SeleniumDriver
from ConfigVars import urls,variables
import time,json
import UtilityPackage.CustomLogger as cl
import logging

class MyAccountPageJT(SeleniumDriver):

    def __init__(self, driver, locator):
        self.driver = driver
        with open(locator) as f:
            data = json.load(f)
        self.locator = data

    log = cl.customLogger(logging.DEBUG)

    def verify_last_booked_ticket(self,movie_name):
        try:
            self.log.info("Going on booking history tab","by clicking  xpath",self.locator["booking_history_tab"]["xpath"])
            self.elementClick(self.locator["booking_history_tab"]["xpath"], locatorType="xpath")
            self.log.info("Waiting for booking history to load")
            time.sleep(30)
            return self.isElementPresent(self.locator["ticket_booking_verification"]["xpath"].format(movie_name), locatorType="xpath")
        except Exception:
            self.log.error("Movie does not exist on Booking history page")

    def apply_selected_offer(self):
        self.elementClick(self.locator["apply_offer"]["xpath"], locatorType="xpath")

    def click_recharge_amount_button(self, amount):
        try:
            self.log.info("Clicking on the recharge amount button")
            self.elementClick(self.locator["rechare_amount_button"]["xpath"].format(amount), locatorType="xpath")
            time.sleep(variables.WAIT)
        except:
            self.log.error("Unable to click on recharge amount button")

    def enter_recharge_amount(self, recharge_amount):
        self.sendKeys(recharge_amount, self.locator["recharge_amount_placeholder"]["xpath"], locatorType="xpath")

    def get_recharge_offers(self, offer_name):
        self.elementClick(self.locator["recharge_offers"]["xpath"].format(offer_name), locatorType="xpath")

    def recharege_via_gift_coupan(self, coupancode):
        try:
            self.log.info("Clicking on Gift Coupan")
            self.elementClick(self.locator["gift_coupan"]["xpath"], locatorType="xpath")
            time.sleep(variables.WAIT)
            self.log.info("Entering Coupan Code",coupancode)
            self.sendKeys(coupancode, self.locator["coupan_code"]["xpath"], locatorType="xpath")
            time.sleep(variables.WAIT)
            self.log.info("Availing coupan code ....")
            self.elementClick(self.locator["apply_code"]["xpath"], locatorType="xpath")
            time.sleep(variables.WAIT)
        except:
            self.log.error("Getting Error while Availing gift coupan")

    def verify_recharge_via_coupan(self):
        return self.isElementPresent(self.locator["verify_gift_card_payment"]["xpath"], locatorType="xpath")

    def click_on_account_statement(self):
        self.log.info("Opening Account statement tab it might take little time to load")
        self.elementClick(self.locator["account_statement_tab"]["xpath"], locatorType="xpath")
        '''self.wait_until_element_gets_visible(self.driver, self.statement_table)'''

    def verify_last_entry_in_account(self):
        try:
            self.log.info("Waiting for Account statement to load")
            #self.waitForElement(self.statement_table, locatorType="xpath", timeout=20)
            self.wait_until_element_gets_visible(self.driver, self.locator["statement_table"]["xpath"])
            self.log.info("Returning the Element atribute value")
        except Exception:
            self.log.error("Account statement didn't loaded in time")

        return self.get_value_of_element(self.locator["last_entry_to_statement"]["xpath"], locatorType="xpath")
from UtilityPackage.SeleniumDriver import SeleniumDriver
from ConfigVars import urls,variables
import time
import UtilityPackage.CustomLogger as cl
import logging

class MyAccountPageJT(SeleniumDriver):

    def __init__(self, driver):
        self.driver = driver

    log = cl.customLogger(logging.DEBUG)


    recharge_offers = "//*[@class='name' and contains(text(),'{0}')]"
    recharge_amount_placeholder = "//*[@class='amount-selector']"
    recharge_with_netbanking="//*[contains(text(),'Recharge with  Net Banking')]"
    apply_offer="//*[contains(text(),'Apply Offer')]"
    gift_coupan = "//*[contains(text(),'Apply a Justickets Gift Card')]"
    coupan_code = "//*[@class='coupon']/input"
    apply_code="//*[@class=' enabled'and contains(text(),'Apply Justickets Gift Card')]"
    verify_gift_card_payment="//*[contains(text(),'Gift card applied')]"
    rechare_amount_button="//*[@class='amount-options']/span[contains(text(),{0})]"
    statement_table="//*[@class='statement']"
    account_statement_tab="//*[contains(text(),'Account Statement')]"
    last_entry_to_statement="//*[@id='justickets']/div/div[2]/div/div[4]/div[2]/table/tbody/tr[2]/td[1]/div/span[1]"
    ticket_booking_verification="//*[@class='title' and contains(text(),'{0}')]"
    booking_history_tab = "//*[contains(text(),'Booking History')]"

    def verify_last_booked_ticket(self,movie_name):
        try:
            self.log.info("Going on booking history tab","by clicking  xpath",self.booking_history_tab)
            self.elementClick(self.booking_history_tab, locatorType="xpath")
            self.log.info("Waiting for booking history to load")
            time.sleep(30)
            return self.isElementPresent(self.ticket_booking_verification.format(movie_name), locatorType="xpath")
        except Exception:
            self.log.error("Movie does not exist on Booking history page")


    def apply_selected_offer(self):
        self.elementClick(self.apply_offer, locatorType="xpath")

    def click_recharge_amount_button(self, amount):
        try:
            self.log.info("Clicking on the recharge amount button")
            self.elementClick(self.rechare_amount_button.format(amount), locatorType="xpath")
            time.sleep(variables.WAIT)
        except:
            self.log.error("Unable to click on recharge amount button")

    def enter_recharge_amount(self, recharge_amount):
        self.sendKeys(recharge_amount, self.recharge_amount_placeholder, locatorType="xpath")

    def get_recharge_offers(self, offer_name):
        self.elementClick(self.recharge_offers.format(offer_name), locatorType="xpath")

    def recharege_via_gift_coupan(self, coupancode):
        try:
            self.log.info("Clicking on Gift Coupan")
            self.elementClick(self.gift_coupan, locatorType="xpath")
            time.sleep(variables.WAIT)
            self.log.info("Entering Coupan Code",coupancode)
            self.sendKeys(coupancode, self.coupan_code, locatorType="xpath")
            time.sleep(variables.WAIT)
            self.log.info("Availing coupan code ....")
            self.elementClick(self.apply_code, locatorType="xpath")
            time.sleep(variables.WAIT)
        except:
            self.log.error("Getting Error while Availing gift coupan")

    def verify_recharge_via_coupan(self):
        return self.isElementPresent(self.verify_gift_card_payment, locatorType="xpath")

    def click_on_account_statement(self):
        self.log.info("Opening Account statement tab it might take little time to load")
        self.elementClick(self.account_statement_tab, locatorType="xpath")
        '''self.wait_until_element_gets_visible(self.driver, self.statement_table)'''

    def verify_last_entry_in_account(self):
        try:
            self.log.info("Waiting for Account statement to load")
            #self.waitForElement(self.statement_table, locatorType="xpath", timeout=20)
            self.wait_until_element_gets_visible(self.driver, self.statement_table)
            self.log.info("Returning the Element atribute value")
        except Exception:
            self.log.error("Account statement didn't loaded in time")

        return self.get_value_of_element(self.last_entry_to_statement, locatorType="xpath")
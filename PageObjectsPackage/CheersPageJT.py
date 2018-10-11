from UtilityPackage.SeleniumDriver import SeleniumDriver
import UtilityPackage.CustomLogger as cl
from ConfigVars.TestConfig import variables
import logging
import json,time,random

"""
PaymentClassJT: Surprise your loved ones on big screens
"""


class CheersAndGreetingsJT(SeleniumDriver):

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver, locator):
        #super().__init__(driver)
        self.driver = driver
        with open(locator) as f:
            data = json.load(f)
        self.locator = data

    def skip_cheers_greetings(self):
        try:
            self.log.info("Skipping the Cheers !!")
            self.elementClick(self.locator["skip_cheers"]["xpath"], locatorType="xpath")
        except:
            self.log.error("Unable to Skip the Cheers Bookings")

    def verify_ticket_booking(self):
        try:
            self.log.info("Checking Element Presence.")
            element = self.isElementPresent(self.locator["skip_cheers"]["xpath"], locatorType="xpath")
            return element
        except:
            self.log.error("Unable to Verify the Presence of element")

    def select_the_greetings_type(self, greetings_type):
        try:
            self.log.info("Selecting the greetings type.")
            self.elementClick(self.locator["select_greetings_type"]["xpath"].format(greetings_type), locatorType="xpath")
            time.sleep(variables.WAIT)
        except:
            self.log.error("Unable to select the greeting type")

    def select_movie_for_cheers(self, movie_name):
        try:
            self.elementClick(self.locator["click_movie"]["xpath"], locatorType="xpath")
            self.sendKeys(movie_name, self.locator["common_search"]["xpath"], locatorType="xpath")
            self.elementClick(self.locator["select_search_result"]["xpath"].format(movie_name), locatorType="xpath")
        except:
            self.log.error("Unable to select movie for cheers")

    def select_theatre_for_cheers(self,theatre_name):
        try:
            self.elementClick(self.locator["click_screens"]["xpath"], locatorType="xpath")
            self.log.info("Verifying element existance")
            if self.isElementPresent(self.locator["common_search"]["xpath"], locatorType="xpath"):
                self.log.info("Search element is there, Searching theatre")
                self.sendKeys(theatre_name, self.locator["common_search"]["xpath"], locatorType="xpath")
            else:
                self.log.info("Search element not found")
            self.getElements(self.locator["screen_list"]["xpath"], locatorType="xpath")[0].click()
            self.log.info("Checking that Above line Working or not")
            self.element_click_with_elment(self.getElements(self.locator["screen_list"]["xpath"], locatorType="xpath")[0])
        except:
            self.log.error("Unable to select theatre for cheers")

    def select_date_for_cheers(self):
        try:
            self.elementClick(self.locator["click_date"]["xpath"], locatorType="xpath")
            self.log.info("Checking that Above line Working or not")
            self.element_click_with_elment(random.choice(self.getElements(self.locator["date_list"]["xpath"], locatorType="xpath")))
        except:
            self.log.error("Unable to select date for cheers")

    def select_show_timing(self):
        try:
            self.elementClick(self.locator["click_show_time"]["xpath"], locatorType="xpath")
            self.log.info("Clicking on show timing")
            self.element_click_with_elment(random.choice(self.getElements(self.locator["select_show_time"]["xpath"], locatorType="xpath")))
        except:
            self.log.error("Unable to select show timing for cheers")

    def select_cheers_templete(self):
        try:
            self.log.info("Selecting the cheers templates ")

            self.element_click_with_elment(
            random.choice(self.getElements(self.locator["select_cheer_templete"]["xpath"],
                                           locatorType="xpath")))
            time.sleep(variables.WAIT)
        except:
            self.log.info("Unable to select the greetings")

    def enter_all_details(self):
        try:
            self.log.info("Verifying that  Preview Exists or not")
            if self.isElementPresent(self.locator["preview"]["xpath"], locatorType="xpath"):
                self.log.info("Preview is present so clicking the Preview")
                self.elementClick(self.locator["preview"]["xpath"], locatorType="xpath")
            else:
                self.log.info("Preview N/A")
            for item in self.getElements(self.locator["common_sender_details"]["xpath"], locatorType="xpath"):
                self.send_keys_with_elment(item,variables.CHEERS_INPUT)
                time.sleep(variables.WAIT)
                # self.log.info("We have entered : ", variables.CHEERS_INPUT)
            self.elementClick(self.locator["preview"]["xpath"], locatorType="xpath")
            time.sleep(variables.WAIT)
            self.elementClick(self.locator["make_payment"]["xpath"], locatorType="xpath")
            time.sleep(variables.WAIT)
        except:
            self.log.error("Error While Entering details")

    def check_slots_availability(self):
        try:
            self.log.info("Checking the slot availability")
        except:
            self.log.info("Slot not available")

    def check_greeting_availability(self):
        try:
            self.log.info("Checking the slot availability")
            return self.isElementPresent(self.locator["choose_greetings"]["xpath"], locatorType="xpath")
        except:
            self.log.error("Getting Error While Checking the isElementPresent")

    def select_the_greetings(self):
        self.log.info("Selecting the slot availability")
        self.elementClick(self.locator["choose_greetings"]["xpath"], locatorType="xpath")

    def customize_greetins(self):
        self.log.info("Customizeing the greetings")
        time.sleep(variables.WAIT)
        self.elementClick(self.locator["customize_greeting"]["xpath"], locatorType="xpath")
from UtilityPackage.SeleniumDriver import SeleniumDriver
from ConfigVars import variables
import json

class JTAssistedBooking(SeleniumDriver):

    def __init__(self, driver, locator):
        #super().__init__(driver)
        self.driver = driver
        with open(locator) as f:
            data = json.load(f)
        self.locator = data

    def book_based_on_release_day(self):
        self.elementClick(self.locator["day_of_release"]["xpath"], locatorType="xpath")

    def confirm__class(self):
        self.elementClick(self.locator["confirm_class"]["xpath"], locatorType="xpath")

    def book_on_selected_day(self):
        self.elementClick(self.locator["select_timing"]["xpath"], locatorType="xpath")

    def select_show_timing(self, day_time, time_interval):
        self.elementClick(self.locator["show_timing"]["xpath"].format(day_time,time_interval), locatorType="xpath")

    def advance_booking_disable(self):
        self.elementClick(self.locator["disable_advance_booking"]["xpath"], locatorType="xpath")

    def select_class(self, class_info):
        self.elementClick(self.locator["choose_class"]["xpath"].format(class_info), locatorType="xpath")

    def select_seats(self, count):
        self.elementClick(self.locator["number_of_seats"]["xpath"].format(count), locatorType="xpath")

    def bookt_ticlket_at_any_amount(self):
        self.elementClick(self.locator["not_mention_max_booking_amount"]["xpath"], locatorType="xpath")

    def pay_with_wallet(self):
        self.elementClick(self.locator["pay_with_jt_wallet"]["xpath"], locatorType="xpath")

    def pay_with_simpl(self):
        self.elementClick("input[type='radio'][value='SZ']", locatorType="css")

    def accept_term_con(self):
        self.elementClick(self.locator["terms_condition"]["xpath"], locatorType="xpath")

    def book_my_tickets(self):
        self.elementClick(self.locator["place_order"]["xpath"], locatorType="xpath")

    def verify_bookings(self):
        element = self.isElementPresent(self.locator["verify_assisted_order"]["xpath"], locatorType="xpath")
        return element

    def advance_booking_enabled(self):
        self.elementClick(self.locator["enable_advance_booking"]["xpath"], locatorType="xpath")

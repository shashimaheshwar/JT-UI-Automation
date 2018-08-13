from UtilityPackage.SeleniumDriver import SeleniumDriver
import json
class SeatLayoutClass(SeleniumDriver):

    def __init__(self, driver, locator):
        #super().__init__(driver)
        self.driver = driver
        with open(locator) as f:
            data = json.load(f)
        self.locator = data

    def confirm_in(self):
        self.elementClick(self.locator["book_now"]["xpath"], locatorType="xpath")

    def select_seats(self, seat_type, seat_number):
        self.elementClick(self.locator["dynamic_seat"]["xpath"].format(seat_type, seat_number), locatorType="xpath")

    def verify_seat(self):
        element=self.isElementPresent(self.locator["verify_seat_confirmation"]["xpath"], locatorType="xpath")
        return element

    def select_free_seating_seat(self, seat_number):
        self.elementClick(self.locator["free_seating_test"]["xpath"].format(seat_number), locatorType="xpath")

    def is_free_seating_layout(self):
        element = self.isElementPresent(self.locator["is_free_seating"]["xpath"], locatorType="xpath")
        return element

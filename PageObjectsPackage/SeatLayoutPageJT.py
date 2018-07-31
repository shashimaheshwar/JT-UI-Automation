from UtilityPackage.SeleniumDriver import SeleniumDriver


class SeatLayoutClass(SeleniumDriver):

    def __init__(self, driver):
        #super().__init__(driver)
        self.driver = driver
    is_free_seating = "//*[@class = 'free-selection']"
    dynamic_seat = "//*[contains(@data-reactid,'{0}') and contains(text(),'{1}')]"
    free_seating = "//*[contains(@class,'count') and contains(text(),{0}) ]"
    free_seating_test = "//*[@id='justickets']/div/div[2]/div/div[3]/div/div[3]/div/div/div[1]/div[2]/div[{0}]"
    book_now = "//*[contains(text(),'Confirm in')]"
    verify_seat_confirmation = "//*[@id='justickets']/div/div[2]/div/div[2]/div/div[4]/span"

    def confirm_in(self):
        self.elementClick(self.book_now, locatorType="xpath")

    def select_seats(self, seat_type, seat_number):
        self.elementClick(self.dynamic_seat.format(seat_type, seat_number), locatorType="xpath")

    def verify_seat(self):
        element=self.isElementPresent(self.verify_seat_confirmation, locatorType="xpath")
        return element

    def select_free_seating_seat(self, seat_number):
        self.elementClick(self.free_seating_test.format(seat_number), locatorType="xpath")

    def is_free_seating_layout(self):
        element = self.isElementPresent(self.is_free_seating, locatorType="xpath")
        return element

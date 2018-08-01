from UtilityPackage.SeleniumDriver import SeleniumDriver
from ConfigVars import variables
import time

class JTAssistedBooking(SeleniumDriver):

    def __init__(self, driver):
        #super().__init__(driver)
        self.driver = driver

    day_of_release = "//*[contains(text(),'Day of Release')]"
    select_day = "//*[contains(text(),'Day of Week')]"
    select_timing = "//*[contains(text(),'1st Day')]"
    show_timing = "//*[contains(text(),'{0}')]/span[contains(text(),'{1}')]"
    choose_city = "//*[@id='justickets']/div/div[2]/div/div[2]/div[2]/div[3]/div/div/div"
    choose_theatre = "//*[@id='justickets']/div/div[2]/div/div[2]/div[2]/div[4]/div/div/div"
    disable_advance_booking = "//*[@id='justickets']/div/div[2]/div/div[2]/div[2]/div[5]/div/span[1]/label"
    enable_advance_booking = "//*[@id='justickets']/div/div[2]/div/div[2]/div[2]/div[5]/div/span[2]/label"
    choose_class = "//*[contains(text(),'{0}')]"
    confirm_class= "/html/body/div[3]/div[2]/button[2]"
    choose_number_of_seat = "//*[@id='justickets']/div/div[2]/div/div[2]/div[2]/div[6]/div/span[2]/label"
    number_of_seats = "//*[@class = 'values squared']/span[{0}]"
    not_mention_max_booking_amount = "//*[@id='justickets']/div/div[2]/div/div[2]/div[2]/div[12]/span[2]/label"
    specify_max_booking_amount = "//*[@id='justickets']/div/div[2]/div/div[2]/div[2]/div[12]/span[3]/label"
    pay_with_jt_wallet = "//*[@id='WL:selectedPaymentMode']"
    pay_with_jt_simpl = "//*[@class = 'custom-radio' and label[contains(text(),'Simpl Zero')]]/span[@class='unchecked']"
    terms_condition = "//*[@class = 'prebook-tnc']/label/input"
    place_order = "//*[contains(text(),'Place My Order')]"
    verify_assisted_order = "//*[contains(text(),'Your order instruction has been successfully registered. " \
                            "Please note that this is not a confirmed ticket. We will notify you via SMS and email" \
                            " as soon as we book your ticket.')]"

    def book_based_on_release_day(self):
        self.elementClick(self.day_of_release, locatorType="xpath")

    def confirm__class(self):
        self.elementClick(self.confirm_class, locatorType="xpath")

    def book_on_selected_day(self):
        self.elementClick(self.select_timing, locatorType="xpath")

    def select_show_timing(self, day_time, time_interval):
        self.elementClick(self.show_timing.format(day_time,time_interval), locatorType="xpath")

    def advance_booking_disable(self):
        self.elementClick(self.disable_advance_booking, locatorType="xpath")

    def select_class(self, class_info):
        self.elementClick(self.choose_class.format(class_info), locatorType="xpath")

    def select_seats(self, count):
        self.elementClick(self.number_of_seats.format(count), locatorType="xpath")

    def bookt_ticlket_at_any_amount(self):
        self.elementClick(self.not_mention_max_booking_amount, locatorType="xpath")

    def pay_with_wallet(self):
        self.elementClick(self.pay_with_jt_wallet, locatorType="xpath")

    def pay_with_simpl(self):
        #self.elementClick(self.pay_with_jt_simpl, locatorType="xpath")
        self.elementClick("input[type='radio'][value='SZ']", locatorType="css")

    def accept_term_con(self):
        self.elementClick(self.terms_condition, locatorType="xpath")

    def book_my_tickets(self):
        self.elementClick(self.place_order, locatorType="xpath")

    def verify_bookings(self):
        element = self.isElementPresent(self.verify_assisted_order, locatorType="xpath")
        return element

    def advance_booking_enabled(self):
        self.elementClick(self.enable_advance_booking, locatorType="xpath")

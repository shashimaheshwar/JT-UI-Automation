from UtilityPackage.SeleniumDriver import SeleniumDriver
from selenium.webdriver.common.action_chains import ActionChains
import time


"""
JT_HOME_PAGE class : Page class which contains all the methods and variables. 
All the methods can be re-used by creating object of this class and calling as object.method()
to execute the test case.
"""


class JTHomePage(SeleniumDriver):

    def __init__(self, driver):
        #super().__init__(driver)
        self.driver = driver

    justickets_home = "//*[@id='justickets']/div/div[1]/div[1]/div/a[2]/img"
    retrieve_booking = "//*[@id='justickets']/div/div[1]/div[1]/div/a[4]/span"
    location = "//*[@id='justickets']/div/div[1]/div[1]/div/a[5]/svg"
    movie_filter = "//*[@id='justickets']/div/div[1]/div[2]/div/div[1]/div/div/div[2]/span"
    movie_input = "//*[@id='justickets']/div/div[1]/div[2]/div/div[1]/div[2]/input"
    movie_filter_default = "//*[@id='justickets']/div/div[1]/div[2]/div/div[1]/div[3]/div/div[2]/span[1]"
    theater_filter = "//*[@id='justickets']/div/div[1]/div[2]/div/div[2]/div/div/div[2]/span"
    theatre_input = "//*[@id='justickets']/div/div[1]/div[2]/div/div[2]/div[2]/input"
    theater_filter_default = "//*[@id='justickets']/div/div[1]/div[2]/div/div[2]/div[3]/div/div[2]/span[1]"
    date_filter = "//*[@id='justickets']/div/div[1]/div[2]/div/div[3]/div/div/div[2]/span"
    date_input = "//*[@id='justickets']/div/div[1]/div[2]/div/div[3]/div"
    date_filter_default = "//*[@id='justickets']/div/div[1]/div[2]/div/div[3]/div[3]/div[1]/div[2]/span"
    time_filter = "//*[@id='justickets']/div/div[1]/div[2]/div/div[4]/div/div/div[2]/span"
    time_filter_default = "XPATH,//*[@id='justickets']/div/div[1]/div[2]/div/div[4]/div[2]/div[1]/div[2]"
    offer_filter = "//*[@id='justickets']/div/div[1]/div[2]/div/div[5]/div/div/div[2]/span"
    offer_filter_default = "//*[@id='justickets']/div/div[1]/div[2]/div/div[5]/div[2]/div[1]/div[2]/span"
    bookings_open = "//*[@id='justickets']/div/div[2]/div/div[2]/div[2]/div[1]/p"
    #assisted_bookings = "//*[contains(text(),'Assisted Booking')]"
    assisted_bookings = "//*[@id='justickets']/div/div[2]/div/div[2]/div[2]/div[2]/p"
    offers = "//*[@id='justickets']/div/div[2]/div/div[2]/div[2]/div[3]/p"
    cheers = "//*[@id='justickets']/div/div[2]/div/div[2]/div[2]/div[4]"
    search_movie = "//*[@id='justickets']/div/div[2]/div/div[2]/div[1]/div/input"
    select_session = "//*[@id='justickets']/div/div[2]/div/div[2]/div[3]/div[2]/div[2]/div/div[2]/a"
    user_avatar_text = "//*[@id='justickets']/div/div[1]/div[1]/div/a[4]/span"
    verify_movie_got_selected="//*[@id='justickets']/div/div[2]/div/div[2]/div[1]/h2"
    movie_search_res = "//*[@id='justickets']/div/div[2]/div/div[2]/div[1]/div[3]/div[1]/div[1]/div[1]/img"
    my_account="//*[contains(text(),'My Account')]"

    def goto_account_page(self):
        self.elementClick(self.my_account, locatorType="xpath")

    def verify_movie_selection(self):
        element = self.isElementPresent(self.verify_movie_got_selected, locatorType="xpath")
        return element

    def filter_with_movie_name(self, movie_name):
        self.elementClick(self.movie_filter,locatorType="xpath")
        self.sendKeys(movie_name, self.movie_input, locatorType="xpath")
        self.elementClick(self.movie_filter_default, locatorType="xpath")

    def movie_filter_with_theatre(self, movie_name, theatre_name):
        self.elementClick(self.theater_filter, locatorType="xpath")
        self.sendKeys(theatre_name, self.theatre_input, locatorType="xpath")
        self.elementClick(self.theater_filter_default, locatorType="xpath")
        time.sleep(3)
        self.elementClick(self.movie_filter, locatorType="xpath")
        self.sendKeys(movie_name, self.movie_input, locatorType="xpath")
        self.elementClick(self.movie_filter_default, locatorType="xpath")

    def movie_filter_with_theatre_date(self,movie_name, theatre_name, date):
        self.movie_filter_with_theatre(movie_name, theatre_name)
        self.elementClick(self.date_filter, locatorType="xpath")
        self.sendKeys(date,self.date_input, locatorType="xpath")
        self.elementClick(self.date_filter_default, locatorType="xpath")

    def select_movie_session(self):
        self.elementClick(self.select_session, locatorType="xpath")

    def jus_tickets_home(self):
        self.elementClick(self.justickets_home, locatorType="xpath")

    def make_assisted_booking(self):
        self.elementClick(self.assisted_bookings, locatorType="xpath")

    def search_for_movie(self, movie_name):
        self.elementClick(self.search_movie, locatorType="xpath")
        time.sleep(5)
        self.sendKeys(movie_name, self.search_movie, locatorType="xpath")

    def select_search_movie(self):
        self.elementClick(self.movie_search_res, locatorType="xpath")

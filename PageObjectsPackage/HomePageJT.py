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

    justickets_home = "//*[@class='logo-holder']/img"
    retrieve_booking = "//*/span[contains(text(),'Retrieve Booking')]"
    location = "//*[@class='action city-selector']"
    movie_filter = "//*[@class='value']/span[contains(text(),'Any Movie')]"
    movie_input = "//*[@class='search' and @placeholder='Search for a movie...']"
    movie_filter_default = "//*[@class='value']/span[contains(text(),'{0}')]"
    theater_filter = "//*[@class='value']/span[contains(text(),'Any Theatre')]"
    theatre_input = "//*[@class='search' and @placeholder='Search for a theatre...']"
    theater_filter_default = "//*[@class='value']/span[contains(text(),'{0}')]"
    date_filter = "//*[@class='value']/span[contains(text(),'Any Date')]"
    date_input = "//*[@class='search' and @placeholder='Search for a date...']"
    date_filter_default = "//*[@class='value']/span[contains(text(),'{0}')]"
    time_filter = "//*[@id='justickets']/div/div[1]/div[2]/div/div[4]/div/div/div[2]/span"
    time_filter_default = "XPATH,//*[@id='justickets']/div/div[1]/div[2]/div/div[4]/div[2]/div[1]/div[2]"
    offer_filter = "//*[@id='justickets']/div/div[1]/div[2]/div/div[5]/div/div/div[2]/span"
    offer_filter_default = "//*[@id='justickets']/div/div[1]/div[2]/div/div[5]/div[2]/div[1]/div[2]/span"
    bookings_open = "//*[@class='active']/p[contains(text(),'Bookings Open')]"
    assisted_bookings = "//*[@class='active']/p[contains(text(),'Assisted Booking')]"
    offers = "//*[@class='active']/p[contains(text(),'Offers')]"
    cheers = "//*[@class='active']/p[contains(text(),'Cheers')]"
    search_movie = "//*[@class='movie-search ']"
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
        self.elementClick(self.movie_filter_default.format(movie_name), locatorType="xpath")

    def movie_filter_with_theatre(self, movie_name, theatre_name):
        self.elementClick(self.theater_filter, locatorType="xpath")
        self.sendKeys(theatre_name, self.theatre_input, locatorType="xpath")
        self.elementClick(self.theater_filter_default.format(theatre_name), locatorType="xpath")
        time.sleep(3)
        self.elementClick(self.movie_filter, locatorType="xpath")
        self.sendKeys(movie_name, self.movie_input, locatorType="xpath")
        self.elementClick(self.movie_filter_default.format(movie_name), locatorType="xpath")

    def movie_filter_with_theatre_date(self,movie_name, theatre_name, date):
        self.movie_filter_with_theatre(movie_name, theatre_name)
        self.elementClick(self.date_filter, locatorType="xpath")
        self.sendKeys(date,self.date_input, locatorType="xpath")
        self.elementClick(self.date_filter_default.format(date), locatorType="xpath")

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

from UtilityPackage.SeleniumDriver import SeleniumDriver
import time,json,random


"""
JT_HOME_PAGE class : Page class which contains all the methods and variables. 
All the methods can be re-used by creating object of this class and calling as object.method()
to execute the test case.
"""


class JTHomePage(SeleniumDriver):

    def __init__(self, driver,locator):
        #super().__init__(driver)
        self.driver = driver
        with open(locator) as f:
            data = json.load(f)
        self.locator = data

    def goto_account_page(self):
        self.elementClick(self.locator["my_account"]["xpath"], locatorType="xpath")

    def verify_movie_selection(self):
        element = self.isElementPresent(self.locator["verify_movie_got_selected"]["xpath"], locatorType="xpath")
        return element

    def filter_with_movie_name(self, movie_name):
        self.elementClick(self.locator["movie_filter"]["xpath"],locatorType="xpath")
        self.sendKeys(movie_name, self.locator["movie_input"]["xpath"], locatorType="xpath")
        self.elementClick(self.locator["movie_filter_default"]["xpath"].format(movie_name), locatorType="xpath")

    def movie_filter_with_theatre(self, movie_name, theatre_name):
        self.elementClick(self.locator["theater_filter"]["xpath"], locatorType="xpath")
        self.sendKeys(theatre_name, self.locator["theatre_input"]["xpath"], locatorType="xpath")
        self.elementClick(self.locator["theater_filter_default"]["xpath"].format(theatre_name), locatorType="xpath")
        time.sleep(3)
        self.elementClick(self.locator["movie_filter"]["xpath"], locatorType="xpath")
        self.sendKeys(movie_name, self.locator["movie_input"]["xpath"], locatorType="xpath")
        self.elementClick(self.locator["movie_filter_default"]["xpath"].format(movie_name), locatorType="xpath")

    def movie_filter_with_theatre_date(self,movie_name, theatre_name, date):
        self.movie_filter_with_theatre(movie_name, theatre_name)
        self.elementClick(self.locator["date_filter"]["xpath"], locatorType="xpath")
        self.sendKeys(date,self.locator["date_input"]["xpath"], locatorType="xpath")
        self.elementClick(self.locator["date_filter_default"]["xpath"].format(date), locatorType="xpath")

    def select_movie_session(self):
        # date_elements = self.getElements(self.locator["locator_date"]["xpath"], locatorType="xpath")
        # element = random.choice(date_elements)
        # self.element_click_with_elment(element)
        # time.sleep(2)
        session_elements = self.getElements(self.locator["locator_session"]["xpath"], locatorType="xpath")
        element = random.choice(session_elements)
        self.element_click_with_elment(element)
        time.sleep(2)

    def select_movie_by_session_id(self, session_id):
        self.elementClick(self.locator["select_session_by_id"]["xpath"].format(session_id), locatorType="xpath")

    def jus_tickets_home(self):
        self.elementClick(self.locator["justickets_home"]["xpath"], locatorType="xpath")

    def make_assisted_booking(self):
        self.elementClick(self.locator["assisted_bookings"]["xpath"], locatorType="xpath")

    def search_for_movie(self, movie_name):
        self.elementClick(self.locator["search_movie"]["xpath"], locatorType="xpath")
        time.sleep(5)
        self.sendKeys(movie_name, self.locator["search_movie"]["xpath"], locatorType="xpath")

    def select_search_movie(self):
        self.elementClick(self.locator["movie_search_res"]["xpath"], locatorType="xpath")

    def select_cheers(self):
        self.elementClick(self.locator["cheers"]["xpath"], locatorType="xpath")
        time.sleep(10)

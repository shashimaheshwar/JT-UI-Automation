from PageObjectsPackage.LoginPageJT import LoginToJT
from PageObjectsPackage.HomePageJT import JTHomePage
from PageObjectsPackage.AssistedBookingJT import JTAssistedBooking
from UtilityPackage.DriverIntialization import DriverIntialization
from ConfigVars import variables,urls
import unittest
import pytest
import time


class JTAssistedBookings(unittest.TestCase):

    baseURL = urls.HOME_PAGE

    @classmethod
    def setUpClass(cls):
        driver = DriverIntialization(urls.HOME_PAGE).return_driver()
        cls.driver = driver
        cls.ltj = LoginToJT(driver, 'PageObjectLocator/LoginPageJT.json')
        cls.homePageObj = JTHomePage(driver, 'PageObjectLocator/HomePageJT.json')
        cls.ab = JTAssistedBooking(driver)
    @classmethod
    def tearDownClass(cls):
        cls.driver.close()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SANITY,SMOKE", reason="")
    @pytest.mark.run(order =1)
    def test_assisted_booking_for_not_released(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(variables.WAIT)
        result = self.ltj.VerifyLogin()
        assert result == True
        time.sleep(variables.WAIT)
        self.homePageObj.make_assisted_booking()
        time.sleep(variables.WAIT)
        self.homePageObj.search_for_movie("GOLD")
        time.sleep(variables.WAIT)
        self.homePageObj.select_search_movie()
        time.sleep(variables.WAIT)
        self.ab.book_based_on_release_day()
        time.sleep(variables.WAIT)
        self.ab.book_on_selected_day()
        time.sleep(variables.WAIT)
        self.ab.select_show_timing("Morning","4am - 12pm")
        time.sleep(variables.WAIT)
        self.ab.advance_booking_disable()
        time.sleep(variables.WAIT)
        self.ab.select_class("Any Class")
        time.sleep(variables.WAIT)
        self.ab.select_seats()
        time.sleep(variables.WAIT)
        self.ab.bookt_ticlket_at_any_amount()
        time.sleep(variables.WAIT)
        self.ab.pay_with_wallet()
        time.sleep(variables.WAIT)
        self.ab.accept_term_con()
        time.sleep(variables.WAIT)
        self.ab.book_my_tickets()
        time.sleep(variables.WAIT)
        assert self.ab.verify_bookings() == True

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION", reason="")
    @pytest.mark.run(order=2)
    def test_assisted_booking_for_not_released_pay_by_simpl(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(variables.WAIT)
        result = self.ltj.VerifyLogin()
        assert result == True
        time.sleep(variables.WAIT)
        self.homePageObj.make_assisted_booking()
        time.sleep(variables.WAIT)
        self.homePageObj.search_for_movie("GOLD")
        time.sleep(variables.WAIT)
        self.homePageObj.select_search_movie()
        time.sleep(variables.WAIT)
        self.ab.book_based_on_release_day()
        time.sleep(variables.WAIT)
        self.ab.book_on_selected_day()
        time.sleep(variables.WAIT)
        self.ab.select_show_timing("Afternoon","11am - 5pm")
        time.sleep(variables.WAIT)
        self.ab.advance_booking_disable()
        time.sleep(variables.WAIT)
        self.ab.select_class("Best Class")
        time.sleep(variables.WAIT)
        self.ab.confirm__class()
        time.sleep(variables.WAIT)
        self.ab.select_seats(variables.WAIT)
        time.sleep(variables.WAIT)
        self.ab.bookt_ticlket_at_any_amount()
        time.sleep(variables.WAIT)
        self.ab.pay_with_simpl()
        time.sleep(variables.WAIT)
        self.ab.accept_term_con()
        time.sleep(variables.WAIT)
        self.ab.book_my_tickets()
        time.sleep(variables.WAIT)
        assert self.ab.verify_bookings() == True

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION", reason="")
    @pytest.mark.run(order =3)
    def test_assisted_booking_advance_booking_allowed(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(variables.WAIT)
        result = self.ltj.VerifyLogin()
        assert result == True
        time.sleep(variables.WAIT)
        self.homePageObj.make_assisted_booking()
        time.sleep(variables.WAIT)
        self.homePageObj.search_for_movie("GOLD")
        time.sleep(variables.WAIT)
        self.homePageObj.select_search_movie()
        time.sleep(variables.WAIT)
        self.ab.book_based_on_release_day()
        time.sleep(variables.WAIT)
        self.ab.book_on_selected_day()
        time.sleep(variables.WAIT)
        self.ab.select_show_timing("Morning","4am - 12pm")
        time.sleep(variables.WAIT)
        self.ab.advance_booking_enabled()
        time.sleep(variables.WAIT)
        self.ab.select_seats(3)
        time.sleep(variables.WAIT)
        self.ab.bookt_ticlket_at_any_amount()
        time.sleep(variables.WAIT)

        self.ab.pay_with_simpl()
        time.sleep(variables.WAIT)
        self.ab.accept_term_con()
        time.sleep(variables.WAIT)
        self.ab.book_my_tickets()
        time.sleep(variables.WAIT)
        #self.driver.close()

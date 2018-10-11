from PageObjectsPackage.LoginPageJT import LoginToJT
from PageObjectsPackage.HomePageJT import JTHomePage
from PageObjectsPackage.PaymentPageJT import PaymentClassJT
from PageObjectsPackage.CheersPageJT import CheersAndGreetingsJT
from UtilityPackage.DriverIntialization import DriverIntialization
from ConfigVars.FrameworkConfig import urls
from ConfigVars.TestConfig import variables
from UtilityPackage import PaymentMethodStatus
import unittest
import pytest
import time,random


class JTCheersTestClass(unittest.TestCase):

    baseURL = urls.HOME_PAGE

    @classmethod
    def setUpClass(cls):
        driver = DriverIntialization(urls.HOME_PAGE).return_driver()
        cls.driver = driver
        cls.ltj = LoginToJT(driver, 'PageObjectLocator/LoginPageJT.json')
        cls.homePageObj = JTHomePage(driver, 'PageObjectLocator/HomePageJT.json')
        cls.pay = PaymentClassJT(driver, 'PageObjectLocator/PaymentPageJT.json')
        cls.cheers = CheersAndGreetingsJT(driver, 'PageObjectLocator/CheersPageJT.json')

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SANITY", reason="")
    @pytest.mark.run(order=1)
    @PaymentMethodStatus.wl_payment
    def test_cheers_booking_wallet_payment(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(variables.WAIT)
        assert self.ltj.VerifyLogin()
        self.homePageObj.select_cheers()
        self.cheers.select_the_greetings_type(variables.GREETING_TYPE)
        time.sleep(variables.WAIT)
        self.cheers.select_movie_for_cheers(variables.MOVIE_NAME)
        time.sleep(variables.WAIT)
        self.cheers.select_theatre_for_cheers(variables.THEATRE_NAME)
        self.cheers.select_date_for_cheers()
        self.cheers.select_show_timing()

        self.cheers.select_cheers_templete()
        self.cheers.enter_all_details()
        self.pay.pay_with_jt_wallet()
        assert self.pay.verify_booking_confirmation() == True
        self.ltj.signout_feature()
        time.sleep(variables.WAIT)

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION", reason="")
    @pytest.mark.run(order=2)
    @PaymentMethodStatus.cc_payment
    def test_cheers_booking_cc_payment(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(variables.WAIT)
        assert self.ltj.VerifyLogin()
        self.homePageObj.select_cheers()
        self.cheers.select_the_greetings_type(variables.GREETING_TYPE)
        time.sleep(variables.WAIT)
        self.cheers.select_movie_for_cheers(variables.MOVIE_NAME)
        time.sleep(variables.WAIT)
        self.cheers.select_theatre_for_cheers(variables.THEATRE_NAME)
        self.cheers.select_date_for_cheers()
        self.cheers.select_show_timing()
        self.cheers.select_cheers_templete()
        self.cheers.enter_all_details()
        self.pay.pay_with_saved_cc_dc()
        assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()
        time.sleep(variables.WAIT)

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION", reason="")
    @pytest.mark.run(order=3)
    @PaymentMethodStatus.pt_payment
    def test_cheers_booking_paytm_payment(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(variables.WAIT)
        assert self.ltj.VerifyLogin()
        self.homePageObj.select_cheers()
        self.cheers.select_the_greetings_type(variables.GREETING_TYPE)
        time.sleep(variables.WAIT)
        self.cheers.select_movie_for_cheers(variables.MOVIE_NAME)
        time.sleep(variables.WAIT)
        self.cheers.select_theatre_for_cheers(variables.THEATRE_NAME)
        self.cheers.select_date_for_cheers()
        self.cheers.select_show_timing()
        self.cheers.select_cheers_templete()
        self.cheers.enter_all_details()
        self.pay.pay_with_paytm()
        assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()
        time.sleep(variables.WAIT)

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION", reason="")
    @pytest.mark.run(order=4)
    @PaymentMethodStatus.pp_payment
    def test_cheers_booking_pp_payment(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(variables.WAIT)
        assert self.ltj.VerifyLogin()
        self.homePageObj.select_cheers()
        self.cheers.select_the_greetings_type(variables.GREETING_TYPE)
        time.sleep(variables.WAIT)
        self.cheers.select_movie_for_cheers(variables.MOVIE_NAME)
        time.sleep(variables.WAIT)
        self.cheers.select_theatre_for_cheers(variables.THEATRE_NAME)
        self.cheers.select_date_for_cheers()
        self.cheers.select_show_timing()
        self.cheers.select_cheers_templete()
        self.cheers.enter_all_details()
        self.pay.pay_with_phonepay_wallet()
        assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()
        time.sleep(variables.WAIT)

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION", reason="")
    @pytest.mark.run(order=5)
    @PaymentMethodStatus.ap_payment
    def test_cheers_booking_ap_payment(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(variables.WAIT)
        assert self.ltj.VerifyLogin()
        self.homePageObj.select_cheers()
        self.cheers.select_the_greetings_type(variables.GREETING_TYPE)
        time.sleep(variables.WAIT)
        self.cheers.select_movie_for_cheers(variables.MOVIE_NAME)
        time.sleep(variables.WAIT)
        self.cheers.select_theatre_for_cheers(variables.THEATRE_NAME)
        self.cheers.select_date_for_cheers()
        self.cheers.select_show_timing()
        self.cheers.select_cheers_templete()
        self.cheers.enter_all_details()
        self.pay.pay_with_amazon()
        assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()
        time.sleep(variables.WAIT)

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION", reason="")
    @pytest.mark.run(order=6)
    @PaymentMethodStatus.simpl_payment
    def test_cheers_booking_simple_payment(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(variables.WAIT)
        assert self.ltj.VerifyLogin()
        self.homePageObj.select_cheers()
        self.cheers.select_the_greetings_type(variables.GREETING_TYPE)
        time.sleep(variables.WAIT)
        self.cheers.select_movie_for_cheers(variables.MOVIE_NAME)
        time.sleep(variables.WAIT)
        self.cheers.select_theatre_for_cheers(variables.THEATRE_NAME)
        self.cheers.select_date_for_cheers()
        self.cheers.select_show_timing()
        self.cheers.select_cheers_templete()
        self.cheers.enter_all_details()
        self.pay.pay_later_by_simpl()
        assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()
        time.sleep(variables.WAIT)
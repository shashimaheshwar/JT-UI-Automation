from PageObjectsPackage.SeatLayoutPageJT import SeatLayoutClass
from PageObjectsPackage.LoginPageJT import LoginToJT
from PageObjectsPackage.HomePageJT import JTHomePage
from PageObjectsPackage.PaymentPageJT import PaymentClassJT
from PageObjectsPackage.MyAccountPage import MyAccountPageJT
from PageObjectsPackage.CheersPageJT import CheersAndGreetingsJT
from PageObjectsPackage.FoodAndBrevrage import FoodAndBrevrageJT
from UtilityPackage.ExractSeatLayoutInformation import ExtractSessionID
from UtilityPackage.DriverIntialization import DriverIntialization
from ConfigVars.FrameworkConfig import urls
from ConfigVars.TestConfig import variables,SessionTypeInfo
from ConfigVars.TestConfig import MyAccountInputs
import unittest
import pytest
import time,random


class JTMyAccountTestClass(unittest.TestCase):

    baseURL = urls.HOME_PAGE

    @classmethod
    def setUpClass(cls):
        driver = DriverIntialization(urls.HOME_PAGE).return_driver()
        cls.driver = driver
        cls.ltj = LoginToJT(driver, 'PageObjectLocator/LoginPageJT.json')
        cls.homePageObj = JTHomePage(driver, 'PageObjectLocator/HomePageJT.json')
        cls.sl = SeatLayoutClass(driver, 'PageObjectLocator/SeatLayoutPageJT.json')
        cls.pay = PaymentClassJT(driver, 'PageObjectLocator/PaymentPageJT.json')
        cls.cheers = CheersAndGreetingsJT(driver, 'PageObjectLocator/CheersPageJT.json')
        cls.utility = ExtractSessionID()
        cls.fnb = FoodAndBrevrageJT(driver, 'PageObjectLocator/FoodAndBrevrage.json')
        cls.account = MyAccountPageJT(driver, 'PageObjectLocator/MyAccountPage.json')

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SANITY", reason="")
    @pytest.mark.run(order=1)
    def test_recharge_with_valid_amount_No_offer_CC_DC(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(variables.WAIT)
        result = self.ltj.VerifyLogin()
        assert result == True
        self.homePageObj.goto_account_page()
        time.sleep(variables.WAIT)
        self.account.enter_recharge_amount(MyAccountInputs.Valid_Recharge_Amount)
        time.sleep(variables.WAIT)
        self.pay.recharge_with_cc_or_dc()
        time.sleep(variables.WAIT)
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION", reason="")
    @pytest.mark.run(order=3)
    def test_recharge_with_valid_amount_No_offer_Gift_Coupan(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(variables.WAIT)
        result = self.ltj.VerifyLogin()
        assert result == True
        self.homePageObj.goto_account_page()
        time.sleep(variables.WAIT)
        self.account.recharege_via_gift_coupan(MyAccountInputs.JusTicet_Gift_Card)
        time.sleep(variables.WAIT)
        if self.account.verify_recharge_via_coupan():
            assert True
        else:
            assert False

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION", reason="")
    @pytest.mark.run(order=2)
    def test_recharge_with_valid_amount_With_offer_CC_DC(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(variables.WAIT)
        result = self.ltj.VerifyLogin()
        assert result == True
        self.homePageObj.goto_account_page()
        time.sleep(variables.WAIT)
        self.account.get_recharge_offers(MyAccountInputs.Recharge_offer_name)
        time.sleep(variables.WAIT)
        self.account.apply_selected_offer()
        time.sleep(variables.WAIT)
        self.account.enter_recharge_amount(MyAccountInputs.Valid_Recharge_Amount)
        time.sleep(variables.WAIT)
        self.pay.recharge_with_cc_or_dc()
        time.sleep(variables.WAIT)
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SANITY", reason="")
    @pytest.mark.run(order=4)
    def test_recharge_with_amount_button_No_offer_CC_DC(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(variables.WAIT)
        result = self.ltj.VerifyLogin()
        assert result == True
        self.homePageObj.goto_account_page()
        time.sleep(variables.WAIT)
        self.account.enter_recharge_amount(MyAccountInputs.Amount_Button.split(",")[random.randint(0, 3)])
        time.sleep(variables.WAIT)
        self.pay.recharge_with_cc_or_dc()
        time.sleep(variables.WAIT)
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION", reason="")
    @pytest.mark.run(order=5)
    def test_recharge_with_amount_button_With_offer_CC_DC(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(variables.WAIT)
        result = self.ltj.VerifyLogin()
        assert result == True
        self.homePageObj.goto_account_page()
        time.sleep(variables.WAIT)
        self.account.get_recharge_offers(MyAccountInputs.Recharge_offer_name)
        time.sleep(variables.WAIT)
        self.account.apply_selected_offer()
        time.sleep(variables.WAIT)
        self.account.enter_recharge_amount(MyAccountInputs.Amount_Button.split(",")[random.randint(0, 3)])
        time.sleep(variables.WAIT)
        self.pay.recharge_with_cc_or_dc()
        time.sleep(variables.WAIT)
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION", reason="")
    @pytest.mark.run(order=6)
    def test_recharge_account_statement(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(variables.WAIT)
        result = self.ltj.VerifyLogin()
        assert result == True
        self.homePageObj.goto_account_page()
        time.sleep(variables.WAIT)
        self.account.click_on_account_statement()
        time.sleep(variables.WAIT)
        if MyAccountInputs.Verify_for_Recharge==self.account.verify_last_entry_in_account():
            assert True
        else:
            assert False

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SANITY", reason="")
    @pytest.mark.run(order=7)
    def test_verify_confirmed_movie(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(5)
        result = self.ltj.VerifyLogin()
        assert result == True
        movie_theatre = SessionTypeInfo.Qota_session
        self.homePageObj.movie_filter_with_theatre(movie_theatre.split(",")[0], movie_theatre.split(",")[1])
        time.sleep(variables.WAIT)
        result = self.homePageObj.verify_movie_selection()
        assert result == True
        self.homePageObj.select_movie_session()
        if self.sl.is_free_seating_layout():
            self.sl.select_free_seating_seat(variables.NUMBER_OF_SEATS)
        else:
            session_d = self.driver.current_url.split("/")[-1]
            seat_info = self.utility.get_seat_avaliable(session_d)

            self.sl.select_seats(seat_info.split("_")[0], seat_info.split("_")[1])
        time.sleep(variables.WAIT)
        self.sl.confirm_in()
        time.sleep(5)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.skip_food_brev()
        time.sleep(variables.WAIT)
        self.pay.pay_with_saved_cc_dc()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation() == True
        else:
            assert self.pay.verify_booking_confirmation() == True

        assert self.account.verify_last_booked_ticket(movie_theatre.split(",")[0])
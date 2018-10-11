from PageObjectsPackage.LoginPageJT import LoginToJT
from PageObjectsPackage.HomePageJT import JTHomePage
from PageObjectsPackage.PaymentPageJT import PaymentClassJT
from PageObjectsPackage.CheersPageJT import CheersAndGreetingsJT
from UtilityPackage.DriverIntialization import DriverIntialization
from PageObjectsPackage.FoodAndBrevrage import FoodAndBrevrageJT
from PageObjectsPackage.SeatLayoutPageJT import SeatLayoutClass
from UtilityPackage.ExractSeatLayoutInformation import ExtractSessionID
from ConfigVars.FrameworkConfig import urls
from ConfigVars.TestConfig import variables,SessionTypeInfo
from UtilityPackage import PaymentMethodStatus
import unittest
import pytest
import time,random


class JTCombineCheersTestClass(unittest.TestCase):

    baseURL = urls.HOME_PAGE

    @classmethod
    def setUpClass(cls):
        driver = DriverIntialization(urls.HOME_PAGE).return_driver()
        cls.driver = driver
        cls.ltj = LoginToJT(driver, 'PageObjectLocator/LoginPageJT.json')
        cls.homePageObj = JTHomePage(driver, 'PageObjectLocator/HomePageJT.json')
        cls.sl = SeatLayoutClass(driver, 'PageObjectLocator/SeatLayoutPageJT.json')
        cls.utility = ExtractSessionID()
        cls.pay = PaymentClassJT(driver, 'PageObjectLocator/PaymentPageJT.json')
        cls.cheers = CheersAndGreetingsJT(driver, 'PageObjectLocator/CheersPageJT.json')
        cls.fnb = FoodAndBrevrageJT(driver, 'PageObjectLocator/FoodAndBrevrage.json')

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
        movie_theatre = SessionTypeInfo.Free_Seating
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
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            time.sleep(variables.LONG_WAIT)
            self.cheers.select_the_greetings()
            self.cheers.select_cheers_templete()
            self.cheers.customize_greetins()
            self.cheers.enter_all_details()
            self.pay.pay_with_jt_wallet()
            assert self.pay.verify_booking_confirmation() == True
        else:
            assert self.pay.verify_booking_confirmation() == True
            pytest.skip("Skipping the Testcases because Slot is not available")
        self.ltj.signout_feature()
        time.sleep(variables.WAIT)

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION", reason="")
    @pytest.mark.run(order=2)
    @PaymentMethodStatus.cc_payment
    def test_cheers_booking_credit_card_payment(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(variables.WAIT)
        assert self.ltj.VerifyLogin()
        movie_theatre = SessionTypeInfo.Free_Seating
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
            time.sleep(variables.LONG_WAIT)
            self.cheers.select_the_greetings()
            self.cheers.select_cheers_templete()
            self.cheers.customize_greetins()
            self.cheers.enter_all_details()
            self.pay.pay_with_saved_cc_dc()
            assert self.pay.verify_booking_confirmation() == True
        else:
            assert self.pay.verify_booking_confirmation() == True
            pytest.skip("Skipping the Testcases because Slot is not available")
        self.ltj.signout_feature()
        time.sleep(variables.WAIT)

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION", reason="")
    @pytest.mark.run(order=3)
    @PaymentMethodStatus.ap_payment
    def test_cheers_booking_amazon_pay_payment(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(variables.WAIT)
        assert self.ltj.VerifyLogin()
        movie_theatre = SessionTypeInfo.Free_Seating
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
        self.pay.pay_with_amazon()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            time.sleep(variables.LONG_WAIT)
            self.cheers.select_the_greetings()
            self.cheers.select_cheers_templete()
            self.cheers.customize_greetins()
            self.cheers.enter_all_details()
            self.pay.pay_with_amazon()
            assert self.pay.verify_booking_confirmation() == True
        else:
            assert self.pay.verify_booking_confirmation() == True
            pytest.skip("Skipping the Testcases because Slot is not available")
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
        self.pay.pay_with_phonepay_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            time.sleep(variables.LONG_WAIT)
            self.cheers.select_the_greetings()
            self.cheers.select_cheers_templete()
            self.cheers.customize_greetins()
            self.cheers.enter_all_details()
            self.pay.pay_with_phonepay_wallet()
            assert self.pay.verify_booking_confirmation() == True
        else:
            assert self.pay.verify_booking_confirmation() == True
            pytest.skip("Skipping the Testcases because Slot is not available")
        self.ltj.signout_feature()
        time.sleep(variables.WAIT)

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION", reason="")
    @pytest.mark.run(order=5)
    @PaymentMethodStatus.pt_payment
    def test_cheers_booking_Paytm_payment(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(variables.WAIT)
        assert self.ltj.VerifyLogin()
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
        self.pay.pay_with_paytm()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            time.sleep(variables.LONG_WAIT)
            self.cheers.select_the_greetings()
            self.cheers.select_cheers_templete()
            self.cheers.customize_greetins()
            self.cheers.enter_all_details()
            self.pay.pay_with_paytm()
            assert self.pay.verify_booking_confirmation() == True
        else:
            assert self.pay.verify_booking_confirmation() == True
            pytest.skip("Skipping the Testcases because Slot is not available")
        self.ltj.signout_feature()
        time.sleep(variables.WAIT)

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION", reason="")
    @pytest.mark.run(order=6)
    @PaymentMethodStatus.simpl_payment
    def test_cheers_booking_csimple_payment(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(variables.WAIT)
        assert self.ltj.VerifyLogin()
        movie_theatre = SessionTypeInfo.Free_Seating
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
        self.pay.pay_later_by_simpl()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            time.sleep(variables.LONG_WAIT)
            self.cheers.select_the_greetings()
            self.cheers.select_cheers_templete()
            self.cheers.customize_greetins()
            self.cheers.enter_all_details()
            self.pay.pay_later_by_simpl()
            assert self.pay.verify_booking_confirmation() == True
        else:
            assert self.pay.verify_booking_confirmation() == True
            pytest.skip("Skipping the Testcases because Slot is not available")
        self.ltj.signout_feature()
        time.sleep(variables.WAIT)
from selenium import webdriver
from PageObjectsPackage.SeatLayoutPageJT import SeatLayoutClass
from PageObjectsPackage.LoginPageJT import LoginToJT
from PageObjectsPackage.HomePageJT import JTHomePage
from PageObjectsPackage.PaymentPageJT import PaymentClassJT
from PageObjectsPackage.CheersPageJT import CheersAndGreetingsJT
from PageObjectsPackage.FoodAndBrevrage import FoodAndBrevrageJT
from ConfigVars.FrameworkConfig import urls
from ConfigVars.TestConfig import variables,SessionTypeInfo,PaymentMethodControl
from UtilityPackage.DriverIntialization import DriverIntialization
from UtilityPackage.ExractSeatLayoutInformation import ExtractSessionID
from UtilityPackage import PaymentMethodStatus
import unittest
import pytest
import time


class JTBookingsMoviePassUser(unittest.TestCase):
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

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION", reason="")
    @pytest.mark.run(order=1)
    def test_JT_Login(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(5)
        result = self.ltj.VerifyLogin()
        assert result == True
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "SANITY", reason="")
    @pytest.mark.run(order=2)
    def test_signout_feature(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(5)
        result = self.ltj.VerifyLogin()
        assert result == True
        self.ltj.signout_feature()
        time.sleep(5)
        result = self.ltj.VerifyLogin()
        assert result == False
        self.ltj.signout_feature()

    @pytest.mark.skipif((variables.TEST_TYPE not in "REGRESSION,SANITY"), reason="")
    @pytest.mark.run(order=3)
    @PaymentMethodStatus.wl_payment
    def test_booking_moviepass_user_Wallet_Qota_session(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(5)
        result=self.ltj.VerifyLogin()
        assert result==True
        movie_theatre = SessionTypeInfo.Qota_session
        self.homePageObj.movie_filter_with_theatre(movie_theatre.split(",")[0], movie_theatre.split(",")[1])
        time.sleep(variables.WAIT)
        result=self.homePageObj.verify_movie_selection()
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
        result=self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.skip_food_brev()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation() == True
        else:
            assert self.pay.verify_booking_confirmation() == True
        self.ltj.signout_feature()

    @pytest.mark.skipif((variables.TEST_TYPE not in "REGRESSION"), reason="")
    @pytest.mark.run(order=4)
    @PaymentMethodStatus.wl_payment
    def test_booking_moviepass_user_Wallet_Free_seating(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(5)
        result = self.ltj.VerifyLogin()
        assert result == True
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
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation() == True
        else:
            assert self.pay.verify_booking_confirmation() == True
        self.ltj.signout_feature()

    @pytest.mark.skipif((variables.TEST_TYPE not in "REGRESSION,SANITY,SMOKE"), reason="")
    @pytest.mark.run(order=5)
    @PaymentMethodStatus.wl_payment
    def test_booking_moviepass_user_Wallet_Advance_Free_seating(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(5)
        result = self.ltj.VerifyLogin()
        assert result == True
        movie_theatre = SessionTypeInfo.Advance_Free_seating
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
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation() == True
        else:
            assert self.pay.verify_booking_confirmation() == True

        self.ltj.signout_feature()

    @pytest.mark.skipif((variables.TEST_TYPE not in "REGRESSION,SANITY,SMOKE"), reason="")
    @pytest.mark.run(order=6)
    @PaymentMethodStatus.wl_payment
    def test_booking_moviepass_user_Wallet_Advance_Qota(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(5)
        result = self.ltj.VerifyLogin()
        assert result == True
        movie_theatre = SessionTypeInfo.Advance_Qota
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
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation() == True
        else:
            assert self.pay.verify_booking_confirmation() == True

        self.ltj.signout_feature()

    @pytest.mark.skipif((variables.TEST_TYPE not in "REGRESSION,SANITY,SMOKE"), reason="")
    @pytest.mark.run(order=7)
    @PaymentMethodStatus.cc_payment
    def test_booking_moviepass_user_CC_Qota_session(self):
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
        self.ltj.signout_feature()

    @pytest.mark.skipif((variables.TEST_TYPE not in "REGRESSION"), reason="")
    @pytest.mark.run(order=8)
    @PaymentMethodStatus.cc_payment
    def test_booking_moviepass_user_CC_Free_seating(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(5)
        result = self.ltj.VerifyLogin()
        assert result == True
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
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation() == True
        else:
            assert self.pay.verify_booking_confirmation() == True
        self.ltj.signout_feature()

    @pytest.mark.skipif((variables.TEST_TYPE not in "REGRESSION,SANITY,SMOKE"), reason="")
    @pytest.mark.run(order=9)
    @PaymentMethodStatus.cc_payment
    def test_booking_moviepass_user_CC_Advance_Free_seating(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(5)
        result = self.ltj.VerifyLogin()
        assert result == True
        movie_theatre = SessionTypeInfo.Advance_Free_seating
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
        self.ltj.signout_feature()

    @pytest.mark.skipif((variables.TEST_TYPE not in "REGRESSION,SANITY,SMOKE,TEST") , reason="")
    @pytest.mark.run(order=10)
    @PaymentMethodStatus.cc_payment
    def test_booking_moviepass_user_CC_Advance_Qota(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(5)
        result = self.ltj.VerifyLogin()
        assert result == True
        movie_theatre = SessionTypeInfo.Advance_Qota
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
        self.ltj.signout_feature()

    @pytest.mark.skipif((variables.TEST_TYPE not in "REGRESSION,SANITY,SMOKE"), reason="")
    @pytest.mark.run(order=11)
    @PaymentMethodStatus.pp_payment
    def test_booking_moviepass_user_PP_Qota_session(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(5)
        result = self.ltj.VerifyLogin()
        assert result == True
        time.sleep(variables.WAIT)
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
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation() == True
        else:
            assert self.pay.verify_booking_confirmation() == True
        self.ltj.signout_feature()

    @pytest.mark.skipif((variables.TEST_TYPE not in "REGRESSION"), reason="")
    @pytest.mark.run(order=12)
    @PaymentMethodStatus.pp_payment
    def test_booking_moviepass_user_PP_Free_seating(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(5)
        result = self.ltj.VerifyLogin()
        assert result == True
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
        self.pay.pay_with_phonepay_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation() == True
        else:
            assert self.pay.verify_booking_confirmation() == True
        self.ltj.signout_feature()

    @pytest.mark.skipif((variables.TEST_TYPE not in "REGRESSION"), reason="")
    @pytest.mark.run(order=13)
    @PaymentMethodStatus.pp_payment
    def test_booking_moviepass_user_PP_Advance_Free_seating(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(5)
        result = self.ltj.VerifyLogin()
        assert result == True
        movie_theatre = SessionTypeInfo.Advance_Free_seating
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
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation() == True
        else:
            assert self.pay.verify_booking_confirmation() == True

    @pytest.mark.skipif((variables.TEST_TYPE not in "REGRESSION"), reason="")
    @pytest.mark.run(order=14)
    @PaymentMethodStatus.pp_payment
    def test_booking_moviepass_user_PP_Advance_Qota(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(5)
        result = self.ltj.VerifyLogin()
        assert result == True
        movie_theatre = SessionTypeInfo.Advance_Qota
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
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation() == True
        else:
            assert self.pay.verify_booking_confirmation() == True

    @pytest.mark.skipif((variables.TEST_TYPE not in "REGRESSION,SANITY"), reason="")
    @pytest.mark.run(order=15)
    @PaymentMethodStatus.simpl_payment
    def test_booking_moviepass_user_Simpl_Qota_session(self):
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
        self.pay.pay_later_by_simpl()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation() == True
        else:
            assert self.pay.verify_booking_confirmation() == True
        self.ltj.signout_feature()

    @pytest.mark.skipif((variables.TEST_TYPE not in "REGRESSION"), reason="")
    @pytest.mark.run(order=16)
    @PaymentMethodStatus.simpl_payment
    def test_booking_moviepass_user_Simpl_Free_seating(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(5)
        result = self.ltj.VerifyLogin()
        assert result == True
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
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation() == True
        else:
            assert self.pay.verify_booking_confirmation() == True
        self.ltj.signout_feature()

    @pytest.mark.skipif((variables.TEST_TYPE not in "REGRESSION"), reason="")
    @pytest.mark.run(order=17)
    @PaymentMethodStatus.simpl_payment
    def test_booking_moviepass_user_Simpl_Advance_Free_seating(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(5)
        result = self.ltj.VerifyLogin()
        assert result == True
        movie_theatre = SessionTypeInfo.Advance_Free_seating
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
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation() == True
        else:
            assert self.pay.verify_booking_confirmation() == True
        self.ltj.signout_feature()

    @pytest.mark.skipif((variables.TEST_TYPE not in "SANITY,REGRESSION"), reason="")
    @pytest.mark.run(order=18)
    @PaymentMethodStatus.pt_payment
    def test_booking_moviepass_user_Paytm_Qota_session(self):
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
        self.pay.pay_with_paytm()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation() == True
        else:
            assert self.pay.verify_booking_confirmation() == True
        self.ltj.signout_feature()

    @pytest.mark.skipif((variables.TEST_TYPE not in "REGRESSION"), reason="")
    @pytest.mark.run(order=19)
    @PaymentMethodStatus.simpl_payment
    def test_booking_moviepass_user_Simpl_Advance_Qota(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(5)
        result = self.ltj.VerifyLogin()
        assert result == True
        movie_theatre = SessionTypeInfo.Advance_Qota
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
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation() == True
        else:
            assert self.pay.verify_booking_confirmation() == True
        self.ltj.signout_feature()

    @pytest.mark.skipif((variables.TEST_TYPE not in "REGRESSION"), reason="")
    @pytest.mark.run(order=20)
    @PaymentMethodStatus.pt_payment
    def test_booking_moviepass_user_Paytm_Free_seating(self):
        self.driver.get(self.baseURL)
        self.ltj.UserLogin(variables.MOVIEPASS_USER_EMAIL, variables.MOVIEPASS_USER_PASSWORD)
        time.sleep(5)
        result = self.ltj.VerifyLogin()
        assert result == True
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
        self.pay.pay_with_paytm()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation() == True
        else:
            assert self.pay.verify_booking_confirmation() == True
        self.ltj.signout_feature()

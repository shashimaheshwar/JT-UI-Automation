from selenium import webdriver
from PageObjectsPackage.SeatLayoutPageJT import SeatLayoutClass
from PageObjectsPackage.LoginPageJT import LoginToJT
from PageObjectsPackage.HomePageJT import JTHomePage
from PageObjectsPackage.PaymentPageJT import PaymentClassJT
from PageObjectsPackage.CheersPageJT import CheersAndGreetingsJT
from PageObjectsPackage.FoodAndBrevrage import FoodAndBrevrageJT
from ConfigVars.FrameworkConfig import urls
from ConfigVars.TestConfig import variables,SessionTypeInfo
from UtilityPackage.DriverIntialization import DriverIntialization
from UtilityPackage.ExractSeatLayoutInformation import ExtractSessionID
import unittest
import pytest
import time


class JTGuestBookingTestClass(unittest.TestCase):
    baseURL = urls.HOME_PAGE
    @classmethod
    def setUpClass(cls):
        driver = DriverIntialization(urls.HOME_PAGE).return_driver()
        cls.driver=driver
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
    def test_booking_as_guest_user_Free_Seating_cc(self):
        self.driver.get(self.baseURL)
        movie_theatre=SessionTypeInfo.Free_Seating
        self.homePageObj.movie_filter_with_theatre(movie_theatre.split(",")[0],movie_theatre.split(",")[1])
        time.sleep(variables.WAIT)
        result = self.homePageObj.verify_movie_selection()
        assert result == True
        self.homePageObj.select_movie_session()
        time.sleep(variables.WAIT)
        if self.sl.is_free_seating_layout():
            self.sl.select_free_seating_seat(variables.NUMBER_OF_SEATS)
        else:
            session_d = self.driver.current_url.split("/")[-1]
            seat_info = self.utility.get_seat_avaliable(session_d)

            self.sl.select_seats(seat_info.split("_")[0], seat_info.split("_")[1])
        time.sleep(variables.WAIT)
        self.sl.confirm_in()
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.skip_food_brev()
        time.sleep(variables.WAIT)
        self.pay.pay_with_cc_dc()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation() == True
        else:
            assert self.pay.verify_booking_confirmation() == True

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION", reason="")
    @pytest.mark.run(order=2)
    def test_booking_guest_user_qota_session_CC(self):
        self.driver.get(self.baseURL)
        movie_theatre = SessionTypeInfo.Qota_session
        self.homePageObj.movie_filter_with_theatre(movie_theatre.split(",")[0], movie_theatre.split(",")[1])
        time.sleep(variables.WAIT)
        result = self.homePageObj.verify_movie_selection()
        assert result == True
        self.homePageObj.select_movie_session()
        time.sleep(variables.WAIT)
        if self.sl.is_free_seating_layout():
            self.sl.select_free_seating_seat(variables.NUMBER_OF_SEATS)
        else:
            session_d = self.driver.current_url.split("/")[-1]
            seat_info = self.utility.get_seat_avaliable(session_d)

            self.sl.select_seats(seat_info.split("_")[0], seat_info.split("_")[1])
        time.sleep(variables.WAIT)
        self.sl.confirm_in()
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.skip_food_brev()
        time.sleep(variables.WAIT)
        self.pay.pay_with_cc_dc()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation() == True
        else:
            assert self.pay.verify_booking_confirmation() == True

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION", reason="")
    @pytest.mark.run(order=3)
    def test_booking_guest_Advance_Free_seating_CC(self):
        self.driver.get(self.baseURL)
        movie_theatre = SessionTypeInfo.Advance_Free_seating
        self.homePageObj.movie_filter_with_theatre(movie_theatre.split(",")[0], movie_theatre.split(",")[1])
        time.sleep(variables.WAIT)
        result = self.homePageObj.verify_movie_selection()
        assert result == True
        self.homePageObj.select_movie_session()
        time.sleep(variables.WAIT)
        if self.sl.is_free_seating_layout():
            self.sl.select_free_seating_seat(variables.NUMBER_OF_SEATS)
        else:
            session_d = self.driver.current_url.split("/")[-1]
            seat_info = self.utility.get_seat_avaliable(session_d)

            self.sl.select_seats(seat_info.split("_")[0], seat_info.split("_")[1])
        time.sleep(variables.WAIT)
        self.sl.confirm_in()
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.skip_food_brev()
        time.sleep(variables.WAIT)
        self.pay.pay_with_cc_dc()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation() == True
        else:
            assert self.pay.verify_booking_confirmation() == True

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SANITY", reason="")
    @pytest.mark.run(order=4)
    def test_booking_guest_Advance_Qota_CC(self):
        self.driver.get(self.baseURL)
        movie_theatre = SessionTypeInfo.Advance_Qota
        self.homePageObj.movie_filter_with_theatre(movie_theatre.split(",")[0], movie_theatre.split(",")[1])
        time.sleep(variables.WAIT)
        result = self.homePageObj.verify_movie_selection()
        assert result == True
        self.homePageObj.select_movie_session()
        time.sleep(variables.WAIT)
        if self.sl.is_free_seating_layout():
            self.sl.select_free_seating_seat(variables.NUMBER_OF_SEATS)
        else:
            session_d = self.driver.current_url.split("/")[-1]
            seat_info = self.utility.get_seat_avaliable(session_d)

            self.sl.select_seats(seat_info.split("_")[0], seat_info.split("_")[1])
        time.sleep(variables.WAIT)
        self.sl.confirm_in()
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.skip_food_brev()
        time.sleep(variables.WAIT)
        self.pay.pay_with_cc_dc()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation() == True
        else:
            assert self.pay.verify_booking_confirmation() == True

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,TESTING", reason="")
    @pytest.mark.run(order=5)
    def test_booking_as_guest_user_PP(self):
        self.driver.get(self.baseURL)
        movie_theatre = SessionTypeInfo.Free_Seating
        self.homePageObj.movie_filter_with_theatre(movie_theatre.split(",")[0], movie_theatre.split(",")[1])
        time.sleep(variables.WAIT)
        result = self.homePageObj.verify_movie_selection()
        assert result == True
        self.homePageObj.select_movie_session()
        time.sleep(variables.WAIT)
        if self.sl.is_free_seating_layout():
            self.sl.select_free_seating_seat(variables.NUMBER_OF_SEATS)
        else:
            session_d = self.driver.current_url.split("/")[-1]
            seat_info = self.utility.get_seat_avaliable(session_d)

            self.sl.select_seats(seat_info.split("_")[0], seat_info.split("_")[1])
        time.sleep(variables.WAIT)
        self.sl.confirm_in()
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.skip_food_brev()
        time.sleep(variables.WAIT)
        self.pay.phone_pay_guest_payment()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation() == True
        else:
            assert self.pay.verify_booking_confirmation() == True

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=6)
    def test_booking_guest_user_qota_session_PP(self):
        self.driver.get(self.baseURL)
        movie_theatre = SessionTypeInfo.Qota_session
        self.homePageObj.movie_filter_with_theatre(movie_theatre.split(",")[0], movie_theatre.split(",")[1])
        time.sleep(variables.WAIT)
        result = self.homePageObj.verify_movie_selection()
        assert result == True
        self.homePageObj.select_movie_session()
        time.sleep(variables.WAIT)
        if self.sl.is_free_seating_layout():
            self.sl.select_free_seating_seat(variables.NUMBER_OF_SEATS)
        else:
            session_d = self.driver.current_url.split("/")[-1]
            seat_info = self.utility.get_seat_avaliable(session_d)

            self.sl.select_seats(seat_info.split("_")[0], seat_info.split("_")[1])
        time.sleep(variables.WAIT)
        self.sl.confirm_in()
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.skip_food_brev()
        time.sleep(variables.WAIT)
        self.pay.phone_pay_guest_payment()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation() == True
        else:
            assert self.pay.verify_booking_confirmation() == True

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=7)
    def test_booking_guest_Advance_Free_seating_PP(self):
        self.driver.get(self.baseURL)
        movie_theatre = SessionTypeInfo.Advance_Free_seating
        self.homePageObj.movie_filter_with_theatre(movie_theatre.split(",")[0], movie_theatre.split(",")[1])
        time.sleep(variables.WAIT)
        result = self.homePageObj.verify_movie_selection()
        assert result == True
        self.homePageObj.select_movie_session()
        time.sleep(variables.WAIT)
        if self.sl.is_free_seating_layout():
            self.sl.select_free_seating_seat(variables.NUMBER_OF_SEATS)
        else:
            session_d = self.driver.current_url.split("/")[-1]
            seat_info = self.utility.get_seat_avaliable(session_d)

            self.sl.select_seats(seat_info.split("_")[0], seat_info.split("_")[1])
        time.sleep(variables.WAIT)
        self.sl.confirm_in()
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.skip_food_brev()
        time.sleep(variables.WAIT)
        self.pay.phone_pay_guest_payment()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation() == True
        else:
            assert self.pay.verify_booking_confirmation() == True

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=8)
    def test_booking_guest_Advance_Qota_PP(self):
        self.driver.get(self.baseURL)
        movie_theatre = SessionTypeInfo.Advance_Qota
        self.homePageObj.movie_filter_with_theatre(movie_theatre.split(",")[0], movie_theatre.split(",")[1])
        time.sleep(variables.WAIT)
        result = self.homePageObj.verify_movie_selection()
        assert result == True
        self.homePageObj.select_movie_session()
        time.sleep(variables.WAIT)
        if self.sl.is_free_seating_layout():
            self.sl.select_free_seating_seat(variables.NUMBER_OF_SEATS)
        else:
            session_d = self.driver.current_url.split("/")[-1]
            seat_info = self.utility.get_seat_avaliable(session_d)

            self.sl.select_seats(seat_info.split("_")[0], seat_info.split("_")[1])
        time.sleep(variables.WAIT)
        self.sl.confirm_in()
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.skip_food_brev()
        time.sleep(variables.WAIT)
        self.pay.phone_pay_guest_payment()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation() == True
        else:
            assert self.pay.verify_booking_confirmation() == True

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,TEST", reason="")
    @pytest.mark.run(order=9)
    def test_booking_as_guest_user_pay_with_amazon(self):
        self.driver.get(self.baseURL)
        movie_theatre = SessionTypeInfo.Free_Seating
        self.homePageObj.movie_filter_with_theatre(movie_theatre.split(",")[0], movie_theatre.split(",")[1])
        time.sleep(variables.WAIT)
        result = self.homePageObj.verify_movie_selection()
        assert result == True
        self.homePageObj.select_movie_session()
        time.sleep(variables.WAIT)
        if self.sl.is_free_seating_layout():
            self.sl.select_free_seating_seat(variables.NUMBER_OF_SEATS)
        else:
            session_d = self.driver.current_url.split("/")[-1]
            seat_info = self.utility.get_seat_avaliable(session_d)

            self.sl.select_seats(seat_info.split("_")[0], seat_info.split("_")[1])
        time.sleep(variables.WAIT)
        self.sl.confirm_in()
        time.sleep(variables.WAIT)
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
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation() == True
        else:
            assert self.pay.verify_booking_confirmation() == True

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,TESTING", reason="")
    @pytest.mark.run(order=10)
    def test_booking_guest_user_qota_session_pay_amazon(self):
        self.driver.get(self.baseURL)
        movie_theatre = SessionTypeInfo.Qota_session
        self.homePageObj.movie_filter_with_theatre(movie_theatre.split(",")[0], movie_theatre.split(",")[1])
        time.sleep(variables.WAIT)
        result = self.homePageObj.verify_movie_selection()
        assert result == True
        self.homePageObj.select_movie_session()
        time.sleep(variables.WAIT)
        if self.sl.is_free_seating_layout():
            self.sl.select_free_seating_seat(variables.NUMBER_OF_SEATS)
        else:
            session_d = self.driver.current_url.split("/")[-1]
            seat_info = self.utility.get_seat_avaliable(session_d)

            self.sl.select_seats(seat_info.split("_")[0], seat_info.split("_")[1])
        time.sleep(variables.WAIT)
        self.sl.confirm_in()
        time.sleep(variables.WAIT)
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
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation() == True
        else:
            assert self.pay.verify_booking_confirmation() == True

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,TESTING", reason="")
    @pytest.mark.run(order=11)
    def test_booking_guest_Advance_Free_seating_pay_amazon(self):
        self.driver.get(self.baseURL)
        movie_theatre = SessionTypeInfo.Advance_Free_seating
        self.homePageObj.movie_filter_with_theatre(movie_theatre.split(",")[0], movie_theatre.split(",")[1])
        time.sleep(variables.WAIT)
        result = self.homePageObj.verify_movie_selection()
        assert result == True
        self.homePageObj.select_movie_session()
        time.sleep(variables.WAIT)
        if self.sl.is_free_seating_layout():
            self.sl.select_free_seating_seat(variables.NUMBER_OF_SEATS)
        else:
            session_d = self.driver.current_url.split("/")[-1]
            seat_info = self.utility.get_seat_avaliable(session_d)

            self.sl.select_seats(seat_info.split("_")[0], seat_info.split("_")[1])
        time.sleep(variables.WAIT)
        self.sl.confirm_in()
        time.sleep(variables.WAIT)
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
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation() == True
        else:
            assert self.pay.verify_booking_confirmation() == True

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,TEST", reason="")
    @pytest.mark.run(order=12)
    def test_booking_guest_Advance_Qota_amazon_pay(self):
        self.driver.get(self.baseURL)
        movie_theatre = SessionTypeInfo.Advance_Qota
        self.homePageObj.movie_filter_with_theatre(movie_theatre.split(",")[0], movie_theatre.split(",")[1])
        time.sleep(variables.WAIT)
        result = self.homePageObj.verify_movie_selection()
        assert result == True
        self.homePageObj.select_movie_session()
        time.sleep(variables.WAIT)
        if self.sl.is_free_seating_layout():
            self.sl.select_free_seating_seat(variables.NUMBER_OF_SEATS)
        else:
            session_d = self.driver.current_url.split("/")[-1]
            seat_info = self.utility.get_seat_avaliable(session_d)

            self.sl.select_seats(seat_info.split("_")[0], seat_info.split("_")[1])
        time.sleep(variables.WAIT)
        self.sl.confirm_in()
        time.sleep(variables.WAIT)
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
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation() == True
        else:
            assert self.pay.verify_booking_confirmation() == True
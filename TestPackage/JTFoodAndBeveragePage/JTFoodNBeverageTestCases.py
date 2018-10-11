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
from ConfigVars.TestConfig import FoodAndBeverageData
from UtilityPackage import PaymentMethodStatus,SessionTypeStatus
import unittest
import pytest
import time,random


class JTFnBTestClass(unittest.TestCase):

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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=1)
    @PaymentMethodStatus.cc_payment
    @SessionTypeStatus.advance_free_seating
    def test_booking_fnb_items_with_tickets_pay_cc_card_advance_Free_Seating(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_saved_cc_dc()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=2)
    @PaymentMethodStatus.cc_payment
    @SessionTypeStatus.advance_free_seating
    def test_booking_add_fnb_item_list_with_tickets_pay_cc_card_advance_Free_Seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_saved_cc_dc()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=3)
    @PaymentMethodStatus.cc_payment
    @SessionTypeStatus.advance_free_seating
    def test_booking_fnb_items_add_n_remove_with_tickets_pay_cc_card_advance_Free_Seating(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=4)
    @PaymentMethodStatus.cc_payment
    @SessionTypeStatus.advance_free_seating
    def test_booking_add_fnb_item_list_n_remove_with_tickets_pay_cc_card_advance_Free_Seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_saved_cc_dc()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=5)
    @PaymentMethodStatus.cc_payment
    @SessionTypeStatus.advance_free_seating
    def test_booking_verify_update_food_cart(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_saved_cc_dc()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=6)
    @PaymentMethodStatus.cc_payment
    @SessionTypeStatus.advance_free_seating
    def test_booking_verify_cancel_changes_in_food_cart_pay_cc_card_advance_Free_Seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.cancel_changes()
        time.sleep(variables.WAIT)
        self.pay.pay_with_saved_cc_dc()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=7)
    @PaymentMethodStatus.cc_payment
    def test_booking_verify_separate_fnb_order_pay_cc_card_advance_Free_Seating(self):
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
        assert result
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.skip_food_brev()
        time.sleep(variables.WAIT)
        self.pay.pay_with_saved_cc_dc()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.account.add_food()
        self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
        self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_saved_cc_dc()
        time.sleep(variables.WAIT)
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=8)
    @PaymentMethodStatus.wl_payment
    @SessionTypeStatus.advance_free_seating
    def test_booking_fnb_items_with_tickets_pay_jt_wallet_Advance_Free_seating(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=9)
    @PaymentMethodStatus.wl_payment
    @SessionTypeStatus.advance_free_seating
    def test_booking_add_fnb_item_list_with_tickets_pay_jt_wallet_Advance_Free_seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=10)
    @PaymentMethodStatus.wl_payment
    @SessionTypeStatus.advance_free_seating
    def test_booking_fnb_items_add_n_remove_with_tickets_pay_jt_wallet_Advance_Free_seating(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=11)
    @PaymentMethodStatus.wl_payment
    @SessionTypeStatus.advance_free_seating
    def test_booking_add_fnb_item_list_n_remove_with_tickets_pay_jt_wallet_Advance_Free_seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=12)
    @PaymentMethodStatus.wl_payment
    @SessionTypeStatus.advance_free_seating
    def test_booking_verify_update_food_cart_pay_jt_wallet_Advance_Free_seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=13)
    @PaymentMethodStatus.wl_payment
    @SessionTypeStatus.advance_free_seating
    def test_booking_verify_cancel_changes_in_food_cart_pay_jt_wallet_Advance_Free_seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.cancel_changes()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=14)
    @PaymentMethodStatus.wl_payment
    @SessionTypeStatus.advance_free_seating
    def test_booking_verify_separate_fnb_order_pay_jt_wallet_Advance_Free_seating(self):
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
        assert result
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.skip_food_brev()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.account.add_food()
        self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
        self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=15)
    @PaymentMethodStatus.simpl_payment
    @SessionTypeStatus.advance_free_seating
    def test_booking_fnb_items_with_tickets_pay_simpl_Advance_Free_seating(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_later_by_simpl()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=16)
    @PaymentMethodStatus.simpl_payment
    @SessionTypeStatus.advance_free_seating
    def test_booking_add_fnb_item_list_with_tickets_pay_simpl_Advance_Free_seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_later_by_simpl()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=17)
    @PaymentMethodStatus.simpl_payment
    @SessionTypeStatus.advance_free_seating
    def test_booking_fnb_items_add_n_remove_with_tickets_pay_simpl_Advance_Free_seating(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_later_by_simpl()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=18)
    @PaymentMethodStatus.simpl_payment
    @SessionTypeStatus.advance_free_seating
    def test_booking_add_fnb_item_list_n_remove_with_tickets_pay_simpl_Advance_Free_seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_later_by_simpl()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=19)
    @PaymentMethodStatus.simpl_payment
    @SessionTypeStatus.advance_free_seating
    def test_booking_verify_update_food_cart_pay_simpl_Advance_Free_seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_later_by_simpl()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=20)
    @PaymentMethodStatus.simpl_payment
    @SessionTypeStatus.advance_free_seating
    def test_booking_verify_cancel_changes_in_food_cart_pay_simpl_Advance_Free_seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.cancel_changes()
        time.sleep(variables.WAIT)
        self.pay.pay_later_by_simpl()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=21)
    @PaymentMethodStatus.simpl_payment
    @SessionTypeStatus.advance_free_seating
    def test_booking_verify_separate_fnb_order_pay_simpl_Advance_Free_seating(self):
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
        assert result
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.skip_food_brev()
        time.sleep(variables.WAIT)
        self.pay.pay_later_by_simpl()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.account.add_food()
        self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
        self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_later_by_simpl()
        time.sleep(variables.WAIT)
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=22)
    @PaymentMethodStatus.pp_payment
    @SessionTypeStatus.advance_free_seating
    def test_booking_fnb_items_with_tickets_pay_phonepay_Advance_Free_seating(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_phonepay_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=23)
    @PaymentMethodStatus.pp_payment
    @SessionTypeStatus.advance_free_seating
    def test_booking_add_fnb_item_list_with_tickets_pay_phonepay_Advance_Free_seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_phonepay_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=24)
    @PaymentMethodStatus.pp_payment
    @SessionTypeStatus.advance_free_seating
    def test_booking_fnb_items_add_n_remove_with_tickets_pay_phonepay_Advance_Free_seating(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_phonepay_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=25)
    @PaymentMethodStatus.pp_payment
    @SessionTypeStatus.advance_free_seating
    def test_booking_add_fnb_item_list_n_remove_with_tickets_pay_phonepay_Advance_Free_seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_phonepay_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=26)
    @PaymentMethodStatus.pp_payment
    @SessionTypeStatus.advance_free_seating
    def test_booking_verify_update_food_cart_pay_phonepay_Advance_Free_seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_phonepay_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=27)
    @PaymentMethodStatus.pp_payment
    @SessionTypeStatus.advance_free_seating
    def test_booking_verify_cancel_changes_in_food_cart_pay_phonepay_Advance_Free_seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.cancel_changes()
        time.sleep(variables.WAIT)
        self.pay.pay_with_phonepay_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=28)
    @PaymentMethodStatus.pp_payment
    @SessionTypeStatus.advance_free_seating
    def test_booking_verify_separate_fnb_order_pay_phonepay_Advance_Free_seating(self):
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
        assert result
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.skip_food_brev()
        time.sleep(variables.WAIT)
        self.pay.pay_with_phonepay_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.account.add_food()
        self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
        self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_phonepay_wallet()
        time.sleep(variables.WAIT)
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=29)
    @PaymentMethodStatus.ap_payment
    @SessionTypeStatus.advance_free_seating
    def test_booking_fnb_items_with_tickets_pay_amazon_Advance_Free_seating(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_amazon()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=30)
    @PaymentMethodStatus.ap_payment
    @SessionTypeStatus.advance_free_seating
    def test_booking_add_fnb_item_list_with_tickets_pay_amazon_Advance_Free_seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_amazon()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=31)
    @PaymentMethodStatus.ap_payment
    @SessionTypeStatus.advance_free_seating
    def test_booking_fnb_items_add_n_remove_with_tickets_pay_amazon_Advance_Free_seating(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_amazon()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=32)
    @PaymentMethodStatus.ap_payment
    @SessionTypeStatus.advance_free_seating
    def test_booking_add_fnb_item_list_n_remove_with_tickets_pay_amazon_Advance_Free_seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_amazon()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=33)
    @PaymentMethodStatus.ap_payment
    @SessionTypeStatus.advance_free_seating
    def test_booking_verify_update_food_cart_pay_amazon_Advance_Free_seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_amazon()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=34)
    @PaymentMethodStatus.ap_payment
    @SessionTypeStatus.advance_free_seating
    def test_booking_verify_cancel_changes_in_food_cart_pay_amazon_Advance_Free_seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.cancel_changes()
        time.sleep(variables.WAIT)
        self.pay.pay_with_amazon()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=35)
    @PaymentMethodStatus.ap_payment
    @SessionTypeStatus.advance_free_seating
    def test_booking_verify_separate_fnb_order_pay_amazon_Advance_Free_seating(self):
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
        assert result
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.skip_food_brev()
        time.sleep(variables.WAIT)
        self.pay.pay_with_amazon()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.account.add_food()
        self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
        self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_amazon()
        time.sleep(variables.WAIT)
        self.ltj.signout_feature()
    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,Test", reason="")
    @pytest.mark.run(order=36)
    @PaymentMethodStatus.cc_payment
    @SessionTypeStatus.free_seating
    def test_booking_fnb_items_with_tickets_pay_cc_card_Free_Seating(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_saved_cc_dc()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,JT_", reason="")
    @pytest.mark.run(order=37)
    @PaymentMethodStatus.cc_payment
    @SessionTypeStatus.free_seating
    def test_booking_add_fnb_item_list_with_tickets_pay_cc_card_Free_Seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_saved_cc_dc()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=38)
    @PaymentMethodStatus.cc_payment
    @SessionTypeStatus.free_seating
    def test_booking_fnb_items_add_n_remove_with_tickets_pay_cc_card_Free_Seating(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=39)
    @PaymentMethodStatus.cc_payment
    @SessionTypeStatus.free_seating
    def test_booking_add_fnb_item_list_n_remove_with_tickets_pay_cc_card_Free_Seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_saved_cc_dc()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=40)
    @PaymentMethodStatus.cc_payment
    @SessionTypeStatus.free_seating
    def test_booking_verify_update_food_cart_pay_cc_card_Free_Seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_saved_cc_dc()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=41)
    @PaymentMethodStatus.cc_payment
    @SessionTypeStatus.free_seating
    def test_booking_verify_cancel_changes_in_food_cart_pay_cc_card_Free_Seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.cancel_changes()
        time.sleep(variables.WAIT)
        self.pay.pay_with_saved_cc_dc()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION", reason="")
    @pytest.mark.run(order=42)
    @PaymentMethodStatus.cc_payment
    @SessionTypeStatus.free_seating
    def test_booking_verify_separate_fnb_order_pay_cc_card_Free_Seating(self):
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
        assert result
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.skip_food_brev()
        time.sleep(variables.WAIT)
        self.pay.pay_with_saved_cc_dc()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.account.add_food()
        self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
        self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_saved_cc_dc()
        time.sleep(variables.WAIT)
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=43)
    @PaymentMethodStatus.wl_payment
    @SessionTypeStatus.free_seating
    def test_booking_fnb_items_with_tickets_pay_jt_wallet_Free_Seating(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,", reason="")
    @pytest.mark.run(order=44)
    @PaymentMethodStatus.wl_payment
    @SessionTypeStatus.free_seating
    def test_booking_add_fnb_item_list_with_tickets_pay_jt_wallet_Free_Seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=45)
    @PaymentMethodStatus.wl_payment
    @SessionTypeStatus.free_seating
    def test_booking_fnb_items_add_n_remove_with_tickets_pay_jt_wallet_Free_Seating(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=46)
    @PaymentMethodStatus.wl_payment
    @SessionTypeStatus.free_seating
    def test_booking_add_fnb_item_list_n_remove_with_tickets_pay_jt_wallet_Free_Seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=47)
    @PaymentMethodStatus.wl_payment
    @SessionTypeStatus.free_seating
    def test_booking_verify_update_food_cart_pay_jt_wallet_Free_Seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=48)
    @PaymentMethodStatus.wl_payment
    @SessionTypeStatus.free_seating
    def test_booking_verify_cancel_changes_in_food_cart_pay_jt_wallet_Free_Seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.cancel_changes()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=49)
    @PaymentMethodStatus.wl_payment
    @SessionTypeStatus.free_seating
    def test_booking_verify_separate_fnb_order_pay_jt_wallet_Free_Seating(self):
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
        assert result
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.skip_food_brev()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.account.add_food()
        self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
        self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION", reason="")
    @pytest.mark.run(order=50)
    @PaymentMethodStatus.simpl_payment
    @SessionTypeStatus.free_seating
    def test_booking_fnb_items_with_tickets_pay_simpl_Free_Seating(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_later_by_simpl()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=51)
    @PaymentMethodStatus.simpl_payment
    @SessionTypeStatus.free_seating
    def test_booking_add_fnb_item_list_with_tickets_pay_simpl_Free_Seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_later_by_simpl()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=52)
    @PaymentMethodStatus.simpl_payment
    @SessionTypeStatus.free_seating
    def test_booking_fnb_items_add_n_remove_with_tickets_pay_simpl_Free_Seating(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_later_by_simpl()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=53)
    @PaymentMethodStatus.simpl_payment
    @SessionTypeStatus.free_seating
    def test_booking_add_fnb_item_list_n_remove_with_tickets_pay_simpl_Free_Seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_later_by_simpl()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,", reason="")
    @pytest.mark.run(order=54)
    @PaymentMethodStatus.simpl_payment
    @SessionTypeStatus.free_seating
    def test_booking_verify_update_food_cart_pay_simpl_Free_Seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_later_by_simpl()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=55)
    @PaymentMethodStatus.simpl_payment
    @SessionTypeStatus.free_seating
    def test_booking_verify_cancel_changes_in_food_cart_pay_simpl_Free_Seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.cancel_changes()
        time.sleep(variables.WAIT)
        self.pay.pay_later_by_simpl()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=56)
    @PaymentMethodStatus.simpl_payment
    @SessionTypeStatus.free_seating
    def test_booking_verify_separate_fnb_order_pay_simpl_Free_Seating(self):
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
        assert result
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.skip_food_brev()
        time.sleep(variables.WAIT)
        self.pay.pay_later_by_simpl()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.account.add_food()
        self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
        self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_later_by_simpl()
        time.sleep(variables.WAIT)
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=57)
    @PaymentMethodStatus.pp_payment
    @SessionTypeStatus.free_seating
    def test_booking_fnb_items_with_tickets_pay_phonepay_Free_Seating(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_phonepay_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=58)
    @PaymentMethodStatus.pp_payment
    @SessionTypeStatus.free_seating
    def test_booking_add_fnb_item_list_with_tickets_pay_phonepay_Free_Seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_phonepay_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=59)
    @PaymentMethodStatus.pp_payment
    @SessionTypeStatus.free_seating
    def test_booking_fnb_items_add_n_remove_with_tickets_pay_phonepay_Free_Seating(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_phonepay_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=60)
    @PaymentMethodStatus.pp_payment
    @SessionTypeStatus.free_seating
    def test_booking_add_fnb_item_list_n_remove_with_tickets_pay_phonepay_Free_Seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_phonepay_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=61)
    @PaymentMethodStatus.pp_payment
    @SessionTypeStatus.free_seating
    def test_booking_verify_update_food_cart_pay_phonepay_Free_Seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_phonepay_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=62)
    @PaymentMethodStatus.pp_payment
    @SessionTypeStatus.free_seating
    def test_booking_verify_cancel_changes_in_food_cart_pay_phonepay_Free_Seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.cancel_changes()
        time.sleep(variables.WAIT)
        self.pay.pay_with_phonepay_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=63)
    @PaymentMethodStatus.pp_payment
    @SessionTypeStatus.free_seating
    def test_booking_verify_separate_fnb_order_pay_phonepay_Free_Seating(self):
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
        assert result
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.skip_food_brev()
        time.sleep(variables.WAIT)
        self.pay.pay_with_phonepay_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.account.add_food()
        self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
        self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_phonepay_wallet()
        time.sleep(variables.WAIT)
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,Test", reason="")
    @pytest.mark.run(order=64)
    @PaymentMethodStatus.pp_payment
    def test_booking_fnb_items_with_tickets_pay_amazon_free_seating(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_amazon()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=65)
    @PaymentMethodStatus.pp_payment
    @SessionTypeStatus.free_seating
    def test_booking_add_fnb_item_list_with_tickets_pay_amazon_free_seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_amazon()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=66)
    @PaymentMethodStatus.pp_payment
    @SessionTypeStatus.free_seating
    def test_booking_fnb_items_add_n_remove_with_tickets_pay_amazon_free_seating(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_amazon()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=67)
    @PaymentMethodStatus.pp_payment
    @SessionTypeStatus.free_seating
    def test_booking_add_fnb_item_list_n_remove_with_tickets_pay_amazon_free_seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_amazon()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=68)
    @PaymentMethodStatus.ap_payment
    @SessionTypeStatus.free_seating
    def test_booking_verify_update_food_cart_pay_amazon_free_seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_amazon()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=69)
    @PaymentMethodStatus.ap_payment
    @SessionTypeStatus.free_seating
    def test_booking_verify_cancel_changes_in_food_cart_pay_amazon_free_seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.cancel_changes()
        time.sleep(variables.WAIT)
        self.pay.pay_with_amazon()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=70)
    @PaymentMethodStatus.ap_payment
    def test_booking_verify_separate_fnb_order_pay_amazon_free_seating(self):
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
        assert result
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.skip_food_brev()
        time.sleep(variables.WAIT)
        self.pay.pay_with_amazon()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.account.add_food()
        self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
        self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_amazon()
        time.sleep(variables.WAIT)
        self.ltj.signout_feature()


    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,Test", reason="")
    @pytest.mark.run(order=71)
    @PaymentMethodStatus.cc_payment
    @SessionTypeStatus.qota
    def test_booking_fnb_items_with_tickets_pay_cc_card_Qota_session(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_saved_cc_dc()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=72)
    @PaymentMethodStatus.cc_payment
    @SessionTypeStatus.qota
    def test_booking_add_fnb_item_list_with_tickets_pay_cc_card_Qota_session(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_saved_cc_dc()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=73)
    @PaymentMethodStatus.cc_payment
    @SessionTypeStatus.qota
    def test_booking_fnb_items_add_n_remove_with_tickets_pay_cc_card_Qota_session(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=74)
    @PaymentMethodStatus.cc_payment
    @SessionTypeStatus.qota
    def test_booking_add_fnb_item_list_n_remove_with_tickets_pay_cc_card_Qota_session(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_saved_cc_dc()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=75)
    @PaymentMethodStatus.cc_payment
    @SessionTypeStatus.qota
    def test_booking_verify_update_food_cart_pay_cc_card_Qota_session(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_saved_cc_dc()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=76)
    @PaymentMethodStatus.cc_payment
    @SessionTypeStatus.qota
    def test_booking_verify_cancel_changes_in_food_cart_pay_cc_card_Qota_session(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.cancel_changes()
        time.sleep(variables.WAIT)
        self.pay.pay_with_saved_cc_dc()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=77)
    @PaymentMethodStatus.cc_payment
    @SessionTypeStatus.qota
    def test_booking_verify_separate_fnb_order_pay_cc_card_Qota_session(self):
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
        assert result
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.skip_food_brev()
        time.sleep(variables.WAIT)
        self.pay.pay_with_saved_cc_dc()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.account.add_food()
        self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
        self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_saved_cc_dc()
        time.sleep(variables.WAIT)
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,Test", reason="")
    @pytest.mark.run(order=78)
    @PaymentMethodStatus.wl_payment
    @SessionTypeStatus.qota
    def test_booking_fnb_items_with_tickets_pay_jt_wallet_Qota_session(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=79)
    @PaymentMethodStatus.wl_payment
    @SessionTypeStatus.qota
    def test_booking_add_fnb_item_list_with_tickets_pay_jt_wallet_Qota_session(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=80)
    @PaymentMethodStatus.wl_payment
    @SessionTypeStatus.qota
    def test_booking_fnb_items_add_n_remove_with_tickets_pay_jt_wallet_Qota_session(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=81)
    @PaymentMethodStatus.wl_payment
    @SessionTypeStatus.qota
    def test_booking_add_fnb_item_list_n_remove_with_tickets_pay_jt_wallet_Qota_session(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=82)
    @PaymentMethodStatus.wl_payment
    @SessionTypeStatus.qota
    def test_booking_verify_update_food_cart_pay_jt_wallet_Qota_session(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=83)
    @PaymentMethodStatus.wl_payment
    @SessionTypeStatus.qota
    def test_booking_verify_cancel_changes_in_food_cart_pay_jt_wallet_Qota_session(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.cancel_changes()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=84)
    @PaymentMethodStatus.wl_payment
    @SessionTypeStatus.qota
    def test_booking_verify_separate_fnb_order_pay_jt_wallet_Qota_session(self):
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
        assert result
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.skip_food_brev()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.account.add_food()
        self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
        self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,Test", reason="")
    @pytest.mark.run(order=85)
    @PaymentMethodStatus.simpl_payment
    @SessionTypeStatus.qota
    def test_booking_fnb_items_with_tickets_pay_simpl_Qota_session(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_later_by_simpl()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=86)
    @SessionTypeStatus.qota
    @PaymentMethodStatus.simpl_payment
    def test_booking_add_fnb_item_list_with_tickets_pay_simpl_Qota_session(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_later_by_simpl()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=87)
    @PaymentMethodStatus.simpl_payment
    @SessionTypeStatus.qota
    def test_booking_fnb_items_add_n_remove_with_tickets_pay_simpl_Qota_session(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_later_by_simpl()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=88)
    @PaymentMethodStatus.simpl_payment
    @SessionTypeStatus.qota
    def test_booking_add_fnb_item_list_n_remove_with_tickets_pay_simpl_Qota_session(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_later_by_simpl()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=89)
    @PaymentMethodStatus.simpl_payment
    @SessionTypeStatus.qota
    def test_booking_verify_update_food_cart_pay_simpl_Qota_session(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_later_by_simpl()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=90)
    @PaymentMethodStatus.simpl_payment
    @SessionTypeStatus.qota
    def test_booking_verify_cancel_changes_in_food_cart_pay_simpl_Qota_session(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.cancel_changes()
        time.sleep(variables.WAIT)
        self.pay.pay_later_by_simpl()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=91)
    @PaymentMethodStatus.simpl_payment
    @SessionTypeStatus.qota
    def test_booking_verify_separate_fnb_order_pay_simpl_Qota_session(self):
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
        assert result
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.skip_food_brev()
        time.sleep(variables.WAIT)
        self.pay.pay_later_by_simpl()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.account.add_food()
        self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
        self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_later_by_simpl()
        time.sleep(variables.WAIT)
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,Test", reason="")
    @pytest.mark.run(order=92)
    @PaymentMethodStatus.pp_payment
    @SessionTypeStatus.qota
    def test_booking_fnb_items_with_tickets_pay_phonepay_Qota_session(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_phonepay_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=93)
    @PaymentMethodStatus.pp_payment
    @SessionTypeStatus.qota
    def test_booking_add_fnb_item_list_with_tickets_pay_phonepay_Qota_session(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_phonepay_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=94)
    @PaymentMethodStatus.pp_payment
    @SessionTypeStatus.qota
    def test_booking_fnb_items_add_n_remove_with_tickets_pay_phonepay_Qota_session(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_phonepay_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=95)
    @PaymentMethodStatus.pp_payment
    @SessionTypeStatus.qota
    def test_booking_add_fnb_item_list_n_remove_with_tickets_pay_phonepay_Qota_session(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_phonepay_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=96)
    @PaymentMethodStatus.pp_payment
    @SessionTypeStatus.qota
    def test_booking_verify_update_food_cart_pay_phonepay_Qota_session(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_phonepay_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SKIP", reason="")
    @pytest.mark.run(order=97)
    @PaymentMethodStatus.pp_payment
    @SessionTypeStatus.qota
    def test_booking_verify_cancel_changes_in_food_cart_pay_phonepay_Qota_session(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.cancel_changes()
        time.sleep(variables.WAIT)
        self.pay.pay_with_phonepay_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=98)
    @PaymentMethodStatus.pp_payment
    @SessionTypeStatus.qota
    def test_booking_verify_separate_fnb_order_pay_phonepay_Qota_session(self):
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
        assert result
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.skip_food_brev()
        time.sleep(variables.WAIT)
        self.pay.pay_with_phonepay_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.account.add_food()
        self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
        self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_phonepay_wallet()
        time.sleep(variables.WAIT)
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION", reason="")
    @pytest.mark.run(order=99)
    @PaymentMethodStatus.ap_payment
    @SessionTypeStatus.qota
    def test_booking_fnb_items_with_tickets_pay_amazon_Qota_session(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_amazon()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=100)
    @PaymentMethodStatus.ap_payment
    @SessionTypeStatus.qota
    def test_booking_add_fnb_item_list_with_tickets_pay_amazon_Qota_session(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_amazon()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=101)
    @PaymentMethodStatus.ap_payment
    @SessionTypeStatus.qota
    def test_booking_fnb_items_add_n_remove_with_tickets_pay_amazon_Qota_session(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_amazon()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=102)
    @PaymentMethodStatus.ap_payment
    @SessionTypeStatus.qota
    def test_booking_add_fnb_item_list_n_remove_with_tickets_pay_amazon_Qota_session(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_amazon()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=103)
    @PaymentMethodStatus.ap_payment
    @SessionTypeStatus.qota
    def test_booking_verify_update_food_cart_pay_amazon_Qota_session(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_amazon()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=104)
    @PaymentMethodStatus.ap_payment
    @SessionTypeStatus.qota
    def test_booking_verify_cancel_changes_in_food_cart_pay_amazon_Qota_session(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.cancel_changes()
        time.sleep(variables.WAIT)
        self.pay.pay_with_amazon()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=105)
    @PaymentMethodStatus.ap_payment
    @SessionTypeStatus.qota
    def test_booking_verify_separate_fnb_order_pay_amazon_Qota_session(self):
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
        assert result
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.skip_food_brev()
        time.sleep(variables.WAIT)
        self.pay.pay_with_amazon()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.account.add_food()
        self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
        self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_amazon()
        time.sleep(variables.WAIT)
        self.ltj.signout_feature()


    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,Test", reason="")
    @pytest.mark.run(order=106)
    @PaymentMethodStatus.cc_payment
    @SessionTypeStatus.advance_qota
    def test_booking_fnb_items_with_tickets_pay_cc_card_Advance_Qota(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_saved_cc_dc()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=107)
    @PaymentMethodStatus.cc_payment
    @SessionTypeStatus.advance_qota
    def test_booking_add_fnb_item_list_with_tickets_pay_cc_card_Advance_Qota(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_saved_cc_dc()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=108)
    @PaymentMethodStatus.cc_payment
    @SessionTypeStatus.advance_qota
    def test_booking_fnb_items_add_n_remove_with_tickets_pay_cc_card_Advance_Qota(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=109)
    @PaymentMethodStatus.cc_payment
    @SessionTypeStatus.advance_qota
    def test_booking_add_fnb_item_list_n_remove_with_tickets_pay_cc_card_Advance_Qota(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_saved_cc_dc()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=110)
    @PaymentMethodStatus.cc_payment
    @SessionTypeStatus.advance_qota
    def test_booking_verify_update_food_cart_pay_cc_card_Advance_Qota(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_saved_cc_dc()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=111)
    @PaymentMethodStatus.cc_payment
    @SessionTypeStatus.advance_qota
    def test_booking_verify_cancel_changes_in_food_cart_pay_cc_card_Advance_Qota(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.cancel_changes()
        time.sleep(variables.WAIT)
        self.pay.pay_with_saved_cc_dc()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=112)
    @PaymentMethodStatus.cc_payment
    @SessionTypeStatus.advance_qota
    def test_booking_verify_separate_fnb_order_pay_cc_card_Advance_Qota(self):
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
        assert result
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.skip_food_brev()
        time.sleep(variables.WAIT)
        self.pay.pay_with_saved_cc_dc()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.account.add_food()
        self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
        self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_saved_cc_dc()
        time.sleep(variables.WAIT)
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,Test", reason="")
    @pytest.mark.run(order=113)
    @PaymentMethodStatus.wl_payment
    @SessionTypeStatus.advance_qota
    def test_booking_fnb_items_with_tickets_pay_jt_wallet_Advance_Qota(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SKIP", reason="")
    @pytest.mark.run(order=114)
    @PaymentMethodStatus.wl_payment
    @SessionTypeStatus.advance_qota
    def test_booking_add_fnb_item_list_with_tickets_pay_jt_wallet_Advance_Qota(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=115)
    @PaymentMethodStatus.wl_payment
    @SessionTypeStatus.advance_qota
    def test_booking_fnb_items_add_n_remove_with_tickets_pay_jt_wallet_Advance_Qota(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=116)
    @PaymentMethodStatus.wl_payment
    @SessionTypeStatus.advance_qota
    def test_booking_add_fnb_item_list_n_remove_with_tickets_pay_jt_wallet_Advance_Qota(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=117)
    @PaymentMethodStatus.wl_payment
    @SessionTypeStatus.advance_qota
    def test_booking_verify_update_food_cart_pay_jt_wallet_Advance_Qota(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=118)
    @PaymentMethodStatus.wl_payment
    @SessionTypeStatus.advance_qota
    def test_booking_verify_cancel_changes_in_food_cart_pay_jt_wallet_Advance_Qota(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.cancel_changes()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=119)
    @PaymentMethodStatus.wl_payment
    @SessionTypeStatus.advance_qota
    def test_booking_verify_separate_fnb_order_pay_jt_wallet_Advance_Qota(self):
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
        assert result
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.skip_food_brev()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.account.add_food()
        self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
        self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_jt_wallet()
        time.sleep(variables.WAIT)
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION", reason="")
    @pytest.mark.run(order=120)
    @PaymentMethodStatus.simpl_payment
    @SessionTypeStatus.advance_qota
    def test_booking_fnb_items_with_tickets_pay_simpl_Advance_Qota(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_later_by_simpl()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=121)
    @PaymentMethodStatus.simpl_payment
    @SessionTypeStatus.advance_qota
    def test_booking_add_fnb_item_list_with_tickets_pay_simpl_Advance_Qota(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_later_by_simpl()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=122)
    @PaymentMethodStatus.simpl_payment
    @SessionTypeStatus.advance_qota
    def test_booking_fnb_items_add_n_remove_with_tickets_pay_simpl_Advance_Qota(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_later_by_simpl()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=123)
    @PaymentMethodStatus.simpl_payment
    @SessionTypeStatus.advance_qota
    def test_booking_add_fnb_item_list_n_remove_with_tickets_pay_simpl_Advance_Qota(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_later_by_simpl()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=124)
    @PaymentMethodStatus.simpl_payment
    @SessionTypeStatus.advance_qota
    def test_booking_verify_update_food_cart_pay_simpl_Advance_Qota(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_later_by_simpl()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=125)
    @PaymentMethodStatus.simpl_payment
    @SessionTypeStatus.advance_qota
    def test_booking_verify_cancel_changes_in_food_cart_pay_simpl_Advance_Qota(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.cancel_changes()
        time.sleep(variables.WAIT)
        self.pay.pay_later_by_simpl()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=126)
    @PaymentMethodStatus.simpl_payment
    @SessionTypeStatus.advance_qota
    def test_booking_verify_separate_fnb_order_pay_simpl_Advance_Qota(self):
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
        assert result
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.skip_food_brev()
        time.sleep(variables.WAIT)
        self.pay.pay_later_by_simpl()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.account.add_food()
        self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
        self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_later_by_simpl()
        time.sleep(variables.WAIT)
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,Test", reason="")
    @pytest.mark.run(order=127)
    @PaymentMethodStatus.pp_payment
    @SessionTypeStatus.advance_qota
    def test_booking_fnb_items_with_tickets_pay_phonepay_Advance_Qota(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_phonepay_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=129)
    @PaymentMethodStatus.pp_payment
    @SessionTypeStatus.advance_qota
    def test_booking_add_fnb_item_list_with_tickets_pay_phonepay_Advance_Qota(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_phonepay_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=130)
    @PaymentMethodStatus.ap_payment
    @SessionTypeStatus.advance_qota
    def test_booking_fnb_items_add_n_remove_with_tickets_pay_phonepay_Advance_Qota(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_phonepay_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=131)
    @SessionTypeStatus.advance_qota
    @PaymentMethodStatus.pp_payment
    def test_booking_add_fnb_item_list_n_remove_with_tickets_pay_phonepay_Advance_Qota(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_phonepay_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=132)
    @PaymentMethodStatus.pp_payment
    @SessionTypeStatus.advance_qota
    def test_booking_verify_update_food_cart_pay_phonepay_Advance_Qota(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_phonepay_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=133)
    @PaymentMethodStatus.pp_payment
    @SessionTypeStatus.advance_qota
    def test_booking_verify_cancel_changes_in_food_cart_pay_phonepay_Advance_Qota(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.cancel_changes()
        time.sleep(variables.WAIT)
        self.pay.pay_with_phonepay_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=134)
    @PaymentMethodStatus.pp_payment
    @SessionTypeStatus.advance_qota
    def test_booking_verify_separate_fnb_order_pay_phonepay_Advance_Qota(self):
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
        assert result
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.skip_food_brev()
        time.sleep(variables.WAIT)
        self.pay.pay_with_phonepay_wallet()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.account.add_food()
        self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
        self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_phonepay_wallet()
        time.sleep(variables.WAIT)
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,Test", reason="")
    @pytest.mark.run(order=135)
    @PaymentMethodStatus.ap_payment
    @SessionTypeStatus.advance_qota
    def test_booking_fnb_items_with_tickets_pay_amazon_Advance_Qota(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_amazon()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SKIP", reason="")
    @pytest.mark.run(order=136)
    @PaymentMethodStatus.ap_payment
    @SessionTypeStatus.advance_qota
    def test_booking_add_fnb_item_list_with_tickets_pay_amazon_Advance_Qota(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_amazon()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=137)
    @PaymentMethodStatus.ap_payment
    @SessionTypeStatus.advance_qota
    def test_booking_fnb_items_add_n_remove_with_tickets_pay_amazon_Advance_Qota(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_amazon()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=155)
    @PaymentMethodStatus.ap_payment
    @SessionTypeStatus.advance_qota
    def test_booking_add_fnb_item_list_n_remove_with_tickets_pay_amazon_Advance_Qota(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_amazon()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=138)
    @PaymentMethodStatus.ap_payment
    @SessionTypeStatus.advance_qota
    def test_booking_verify_update_food_cart_pay_amazon_Advance_Qota(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_amazon()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=139)
    @PaymentMethodStatus.ap_payment
    @SessionTypeStatus.advance_qota
    def test_booking_verify_cancel_changes_in_food_cart_pay_amazon_Advance_Qota(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.cancel_changes()
        time.sleep(variables.WAIT)
        self.pay.pay_with_amazon()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,", reason="")
    @pytest.mark.run(order=140)
    @PaymentMethodStatus.ap_payment
    @SessionTypeStatus.advance_qota
    def test_booking_verify_separate_fnb_order_pay_amazon_Advance_Qota(self):
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
        assert result
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.skip_food_brev()
        time.sleep(variables.WAIT)
        self.pay.pay_with_amazon()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.account.add_food()
        self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
        self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_amazon()
        time.sleep(variables.WAIT)
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SANITY", reason="")
    @pytest.mark.run(order=141)
    @PaymentMethodStatus.pt_payment
    @SessionTypeStatus.free_seating
    def test_booking_fnb_items_with_tickets_pay_with_paytm_Free_Seating(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_paytm()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION", reason="")
    @pytest.mark.run(order=142)
    @PaymentMethodStatus.pt_payment
    @SessionTypeStatus.free_seating
    def test_booking_add_fnb_item_list_with_tickets_pay_with_paytm_Free_Seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_paytm()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION", reason="")
    @pytest.mark.run(order=143)
    @PaymentMethodStatus.pt_payment
    @SessionTypeStatus.free_seating
    def test_booking_fnb_items_add_n_remove_with_tickets_pay_with_paytm_Free_Seating(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_paytm()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION", reason="")
    @pytest.mark.run(order=144)
    @PaymentMethodStatus.pt_payment
    @SessionTypeStatus.free_seating
    def test_booking_add_fnb_item_list_n_remove_with_tickets_pay_with_paytm_Free_Seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_paytm()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION", reason="")
    @pytest.mark.run(order=145)
    @PaymentMethodStatus.pt_payment
    @SessionTypeStatus.free_seating
    def test_booking_verify_update_food_cart_pay_with_paytm_Free_Seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_paytm()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION", reason="")
    @pytest.mark.run(order=146)
    @PaymentMethodStatus.pt_payment
    @SessionTypeStatus.free_seating
    def test_booking_verify_cancel_changes_in_food_cart_pay_with_paytm_Free_Seating(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.cancel_changes()
        time.sleep(variables.WAIT)
        self.pay.pay_with_paytm()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION", reason="")
    @pytest.mark.run(order=147)
    @PaymentMethodStatus.pt_payment
    @SessionTypeStatus.free_seating
    def test_booking_verify_separate_fnb_order_pay_with_paytm_Free_Seating(self):
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
        assert result
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.skip_food_brev()
        time.sleep(variables.WAIT)
        self.pay.pay_with_paytm()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.account.add_food()
        self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
        self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_paytm()
        time.sleep(variables.WAIT)
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SANITY", reason="")
    @pytest.mark.run(order=148)
    @PaymentMethodStatus.pt_payment
    @SessionTypeStatus.qota
    def test_booking_fnb_items_with_tickets_pay_with_paytm_Qota_session(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_paytm()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION", reason="")
    @pytest.mark.run(order=149)
    @PaymentMethodStatus.pt_payment
    @SessionTypeStatus.qota
    def test_booking_add_fnb_item_list_with_tickets_pay_with_paytm_Qota_session(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_paytm()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION", reason="")
    @pytest.mark.run(order=150)
    @PaymentMethodStatus.pt_payment
    @SessionTypeStatus.qota
    def test_booking_fnb_items_add_n_remove_with_tickets_pay_with_paytm_Qota_session(self):
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
        time.sleep(variables.WAIT)
        result = self.sl.verify_seat()
        assert result == True
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_paytm()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION", reason="")
    @pytest.mark.run(order=151)
    @PaymentMethodStatus.pt_payment
    @SessionTypeStatus.qota
    def test_booking_add_fnb_item_list_n_remove_with_tickets_pay_with_paytm_Qota_session(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_paytm()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION", reason="")
    @pytest.mark.run(order=152)
    @PaymentMethodStatus.pt_payment
    @SessionTypeStatus.qota
    def test_booking_verify_update_food_cart_pay_with_paytm_Qota_session(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_paytm()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION", reason="")
    @pytest.mark.run(order=153)
    @PaymentMethodStatus.pt_payment
    @SessionTypeStatus.qota
    def test_booking_verify_cancel_changes_in_food_cart_pay_with_paytm_Qota_session(self):
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
            self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
            self.fnb.remove_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_remove)
            self.fnb.confirm_order()
            self.fnb.manage_order()
            self.fnb.add_fnb_items(FoodAndBeverageData.item, FoodAndBeverageData.no_of_item_add)
            self.fnb.cancel_changes()
        time.sleep(variables.WAIT)
        self.pay.pay_with_paytm()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.ltj.signout_feature()

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION", reason="")
    @pytest.mark.run(order=154)
    @PaymentMethodStatus.pt_payment
    @SessionTypeStatus.qota
    def test_booking_verify_separate_fnb_order_pay_with_paytm_Qota_session(self):
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
        assert result
        time.sleep(variables.WAIT)
        if self.fnb.verify_existence_fnb():
            self.fnb.skip_food_brev()
        time.sleep(variables.WAIT)
        self.pay.pay_with_paytm()
        time.sleep(variables.WAIT)
        result = self.cheers.verify_ticket_booking()
        if result:
            self.cheers.skip_cheers_greetings()
            assert self.pay.verify_booking_confirmation()
        else:
            assert self.pay.verify_booking_confirmation()
        self.account.add_food()
        self.fnb.add_fnb_items_list(FoodAndBeverageData.itemList, FoodAndBeverageData.no_of_item_add)
        self.fnb.confirm_order()
        time.sleep(variables.WAIT)
        self.pay.pay_with_paytm()
        time.sleep(variables.WAIT)
        self.ltj.signout_feature()
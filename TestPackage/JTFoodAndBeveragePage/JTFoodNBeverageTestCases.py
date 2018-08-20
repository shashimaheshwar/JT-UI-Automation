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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,Test", reason="")
    @pytest.mark.run(order=1)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=2)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=5)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=6)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=7)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,Test", reason="")
    @pytest.mark.run(order=8)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=9)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=12)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=13)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=14)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=15)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=16)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=19)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=20)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=21)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,Test", reason="")
    @pytest.mark.run(order=22)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=23)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=26)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=27)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=28)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=33)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=34)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=35)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=37)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=40)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=41)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=42)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=44)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=47)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=48)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=49)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,Test", reason="")
    @pytest.mark.run(order=50)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=51)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=54)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=55)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=56)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=58)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=61)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=62)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=63)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=65)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=68)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=69)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=70)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=72)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=75)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=76)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=77)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=79)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=82)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=84)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=86)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=89)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=90)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=91)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=93)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=96)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=98)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE", reason="")
    @pytest.mark.run(order=99)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=100)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=103)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=104)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=105)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=107)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=110)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=111)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=112)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=117)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=118)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=119)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,Test", reason="")
    @pytest.mark.run(order=120)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=121)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=124)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=125)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=126)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=129)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=132)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=133)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=134)
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
    @pytest.mark.run(order=128)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=138)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=139)
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

    @pytest.mark.skipif(variables.TEST_TYPE not in "REGRESSION,SMOKE,SANITY", reason="")
    @pytest.mark.run(order=140)
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

from UtilityPackage.SeleniumDriver import SeleniumDriver
from ConfigVars.TestConfig import variables
import time,json

"""
PaymentClassJT: All different kind of payment method are there in this.
"""


class PaymentClassJT(SeleniumDriver):

    def __init__(self, driver, locator):
        #super().__init__(driver)
        self.driver = driver
        with open(locator) as f:
            data = json.load(f)
        self.locator = data

    def recharge_with_cc_or_dc(self):
        self.elementClick(self.locator["recharge_with_cc_dc"]["xpath"], locatorType="xpath")
        time.sleep(variables.WAIT)
        self.sendKeys(variables.CC_NUMBER, self.locator["card_num_loc"]["xpath"], locatorType="xpath")
        time.sleep(variables.WAIT)
        self.sendKeys(variables.EXPIREY_DATE, self.locator["expiry_date_loc"]["xpath"], locatorType="xpath")
        time.sleep(variables.WAIT)
        self.sendKeys(variables.CVV, self.locator["CC_CVV"]["xpath"], locatorType="xpath")
        self.elementClick(self.locator["make_payment"]["xpath"], locatorType="xpath")
        time.sleep(variables.WAIT)
        self.sendKeys(variables.CC_PIN, self.locator["cc_pin"]["xpath"], locatorType="id")
        self.elementClick(self.locator["cc_submit"]["xpath"], locatorType="id")
        time.sleep(variables.WAIT)

    def pay_with_saved_cc_dc(self):
        self.elementClick(self.locator["pay_via_justpay"]["xpath"], locatorType="xpath")
        time.sleep(variables.WAIT)
        self.elementClick(self.locator["use_saved_card_details"]["xpath"], locatorType="xpath")
        time.sleep(variables.WAIT)
        self.elementClick(self.locator["select_saved_card"]["xpath"], locatorType="xpath")
        time.sleep(variables.WAIT)
        self.sendKeys(variables.CVV, self.locator["Card_CVV"]["xpath"], locatorType="xpath")
        self.elementClick(self.locator["make_payment"]["xpath"], locatorType="xpath")
        time.sleep(variables.WAIT)
        self.sendKeys(variables.CC_PIN, self.locator["cc_pin"]["id"], locatorType="id")
        self.elementClick(self.locator["cc_submit"]["id"], locatorType="id")
        time.sleep(variables.WAIT)

    def pay_with_jt_wallet(self):
        self.elementClick(self.locator["make_payment"]["xpath"], locatorType="xpath")

    def pay_with_phonepay_wallet(self):
        self.elementClick(self.locator["pay_via_phonepay"]["xpath"], locatorType="xpath")
        self.elementClick(self.locator["make_payment"]["xpath"], locatorType="xpath")
        self.elementClick(self.locator["pay"]["xpath"], locatorType="xpath")

    def verify_payment_confirmation(self):
        element=self.isElementPresent(self.locator["verify_payment"]["xpath"],locatorType="xpath")
        return element

    def verify_amazon_payment_page(self):
        return self.isElementPresent(self.locator["pay_now_amazon"]["xpath"], locatorType="xpath")

    def verify_pp_pay_element(self):
        return self.isElementPresent(self.locator["pay"]["xpath"], locatorType="xpath")

    def pay_with_cc_dc(self):
        self.elementClick(self.locator["pay_via_justpay"]["xpath"],locatorType="xpath")
        time.sleep(variables.WAIT)
        self.sendKeys(variables.CC_NUMBER, self.locator["card_number"]["xpath"], locatorType="xpath")
        self.sendKeys(variables.EXPIREY_DATE, self.locator["expiry_date"]["xpath"], locatorType="xpath")
        self.sendKeys(variables.CVV, self.locator["cvv_number"]["xpath"], locatorType="xpath")
        self.sendKeys(variables.USER_NAME, self.locator["user_name"]["xpath"], locatorType="xpath")
        self.sendKeys(variables.MOVIEPASS_USER_EMAIL, self.locator["user_email"]["xpath"], locatorType="xpath")
        self.sendKeys(variables.MOBILE_NUMBER, self.locator["user_mobile"]["xpath"], locatorType="xpath")
        self.elementClick(self.locator["make_payment"]["xpath"], locatorType="xpath")
        time.sleep(variables.WAIT)
        self.sendKeys(variables.CC_PIN, self.locator["cc_pin"]["id"], locatorType="id")
        self.elementClick(self.locator["cc_submit"]["id"], locatorType="id")
        time.sleep(variables.WAIT)

    def verify_booking_confirmation(self):
        element = self.isElementPresent(self.locator["verify_ticket_booking"]["xpath"], locatorType="xpath")
        return element

    def pay_later_by_simpl(self):
        self.elementClick(self.locator["pay_with_simpl"]["xpath"], locatorType="xpath")
        time.sleep(variables.WAIT)
        if self.isElementPresent(self.locator["link_account_simpl"]["xpath"], locatorType="xpath"):
            assert False
        else:
            self.elementClick(self.locator["pay_later"]["xpath"], locatorType="xpath")

    def phone_pay_guest_payment(self):
        self.elementClick(self.locator["pay_via_phonepay"]["xpath"], locatorType="xpath")
        self.sendKeys(variables.USER_NAME, self.locator["name_for_ticket_detail"]["xpath"], locatorType="xpath")
        self.sendKeys(variables.USER_EMAIL, self.locator["email_for_ticket_detail"]["xpath"], locatorType="xpath")
        self.sendKeys(variables.MOBILE_NUMBER, self.locator["mobile_for_ticket_details"]["xpath"], locatorType="xpath")
        self.elementClick(self.locator["make_payment"]["xpath"], locatorType="xpath")
        time.sleep(variables.WAIT)
        if self.verify_pp_pay_element():
            self.elementClick(self.locator["pay"]["xpath"], locatorType="xpath")
        else:
            self.elementClick(self.locator["use_pp_password"]["id"], locatorType="id")
            time.sleep(variables.WAIT)
            self.sendKeys(variables.PHONE_PAY_PASS, self.locator["phone_pay_pin"]["id"], locatorType="id")
            self.elementClick(self.locator["pp_login"]["id"], locatorType="id")
            time.sleep(variables.WAIT)
            self.elementClick(self.locator["pay"]["xpath"], locatorType="xpath")
            time.sleep(variables.WAIT)

    def pay_with_amazon(self):
        self.elementClick(self.locator["amazon_pay"]["xpath"], locatorType="xpath")
        time.sleep(variables.WAIT)
        self.sendKeys(variables.USER_NAME, self.locator["name_for_ticket_detail"]["xpath"], locatorType="xpath")
        self.sendKeys(variables.USER_EMAIL, self.locator["email_for_ticket_detail"]["xpath"], locatorType="xpath")
        self.sendKeys(variables.MOBILE_NUMBER, self.locator["mobile_for_ticket_details"]["xpath"], locatorType="xpath")
        self.elementClick(self.locator["make_payment"]["xpath"], locatorType="xpath")
        time.sleep(variables.WAIT)
        if self.verify_amazon_payment_page():
            self.elementClick(self.locator["pay_now_amazon"]["xpath"], locatorType="xpath")
            time.sleep(variables.WAIT)
        else:
            self.sendKeys(variables.AMAZON_USER, self.locator["amazon_user"]["id"], locatorType="id")
            self.sendKeys(variables.AMAZON_PASSWORD, self.locator["amazon_passwprd"]["id"], locatorType="id")
            self.elementClick(self.locator["amazon_singin"]["id"], locatorType="id")
            time.sleep(variables.WAIT)
            self.elementClick(self.locator["pay_now_amazon"]["xpath"], locatorType="xpath")
            time.sleep(variables.WAIT)
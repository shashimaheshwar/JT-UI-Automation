from UtilityPackage.SeleniumDriver import SeleniumDriver
from ConfigVars import variables
import time

"""
PaymentClassJT: All different kind of payment method are there in this.
"""


class PaymentClassJT(SeleniumDriver):

    def __init__(self, driver):
        #super().__init__(driver)
        self.driver = driver

    pay_via_jt_wallet = "//*[@id='justickets']/div/div[2]/div/div[3]/div[1]/div[2]/div[1]/div/div/div[1]"
    make_payment = "//*[contains(@class,'enabled') and contains(text(),'Make Payment')]"
    pay_via_justpay = "//*[@id='justickets']/div/div[2]/div/div[3]/div[1]/div[2]/div[2]/div/div/div[1]"
    card_number = "//*[@id='justickets']/div/div[2]/div/div[3]/div[1]/div[2]/div[2]/form/div[1]/input"
    expiry_date = "//*[@id='justickets']/div/div[2]/div/div[3]/div[1]/div[2]/div[2]/form/div[2]/div[1]/input"
    cvv_number = "//*[@id='justickets']/div/div[2]/div/div[3]/div[1]/div[2]/div[2]/form/div[2]/div[2]/input"
    user_name = "//*[@id='justickets']/div/div[2]/div/div[3]/div[1]/div[2]/div[2]/form/div[3]/input[1]"
    user_email = "//*[@id='justickets']/div/div[2]/div/div[3]/div[1]/div[2]/div[2]/form/div[3]/input[2]"
    user_mobile = "//*[@id='justickets']/div/div[2]/div/div[3]/div[1]/div[2]/div[2]/form/div[3]/div/input"
    pay_via_phonepay = "//*[contains(text(),'Pay with  PhonePe - BHIM UPI/Cards/Wallet')]"
    phone_pay_number = "//*[@id='justickets']/div/div[2]/div/div[3]/div[1]/div[2]/div[8]/form/div[1]/div[2]/div/div[1]"
    name_for_ticket_detail = "//*[@class='banking']/div[1]/input[1]"
    email_for_ticket_detail = "//*[@class='banking']/div[1]/input[2]"
    mobile_for_ticket_details= "//*[@class='banking']/div[1]/div/input"
    use_pp_password= "loginWithPasswordToggle"
    pp_login="onboardingFormSubmitBtn"
    pay = "//*[@id='paySubmitButton']"
    phone_pay_pin="password"
    cc_pin = "txtPassword"
    cc_submit = "cmdSubmit"
    pay_with_simpl = "//*[contains(text(),'Pay Later with Simpl')]"
    link_account_simpl = "//*[contains(text(),'Link Account & Pay Later')]"
    pay_later = "//*[contains(text(),'Pay Later') and @class=' enabled']"
    verify_payment = "//*[@id='justickets']/div/div[2]/div/div[2]/div[2]/div[2]/img"
    verify_ticket_booking = "//*[contains(text(),'Ticket')]"
    amazon_pay="//*[contains(text(),'Pay with  Amazon')]"
    pay_now_amazon="//*[@id='pay_now_desktop']/span/input"
    amazon_user="ap_email"
    amazon_passwprd="ap_password"
    amazon_singin="signInSubmit"
    use_saved_card_details="//*[contains(text(),'Use a Saved Card')]"
    select_saved_card = "//*[@id='justickets']/div/div[2]/div/div[3]/div[1]/div[2]/div[2]/form/div[1]/div[2]"
    Card_CVV="//*[@id='justickets']/div/div[2]/div/div[3]/div[1]/div[2]/div[2]/form/div[2]/div/input"
    card_num_loc = "//*[@class='card']/input[@type='tel']"
    expiry_date_loc = "//*[@class='half']/input[@type='tel']"
    CC_CVV = "//*[@class='half']/input[@type='password']"
    recharge_with_cc_dc = "//*[contains(text(),'Recharge with  Credit / Debit card')]"

    def recharge_with_cc_or_dc(self):
        self.elementClick(self.recharge_with_cc_dc, locatorType="xpath")
        time.sleep(variables.WAIT)
        self.sendKeys(variables.CC_NUMBER, self.card_num_loc, locatorType="xpath")
        time.sleep(variables.WAIT)
        self.sendKeys(variables.EXPIREY_DATE, self.expiry_date_loc, locatorType="xpath")
        time.sleep(variables.WAIT)
        self.sendKeys(variables.CVV, self.CC_CVV, locatorType="xpath")
        self.elementClick(self.make_payment, locatorType="xpath")
        time.sleep(variables.WAIT)
        self.sendKeys(variables.CC_PIN, self.cc_pin, locatorType="id")
        self.elementClick(self.cc_submit, locatorType="id")
        time.sleep(variables.WAIT)

    def pay_with_saved_cc_dc(self):
        self.elementClick(self.pay_via_justpay, locatorType="xpath")
        time.sleep(variables.WAIT)
        self.elementClick(self.use_saved_card_details, locatorType="xpath")
        time.sleep(variables.WAIT)
        self.elementClick(self.select_saved_card, locatorType="xpath")
        time.sleep(variables.WAIT)
        self.sendKeys(variables.CVV, self.Card_CVV, locatorType="xpath")
        self.elementClick(self.make_payment, locatorType="xpath")
        time.sleep(variables.WAIT)
        self.sendKeys(variables.CC_PIN, self.cc_pin, locatorType="id")
        self.elementClick(self.cc_submit, locatorType="id")
        time.sleep(variables.WAIT)

    def pay_with_jt_wallet(self):
        self.elementClick(self.make_payment, locatorType="xpath")

    def pay_with_phonepay_wallet(self):
        self.elementClick(self.pay_via_phonepay, locatorType="xpath")
        self.elementClick(self.make_payment, locatorType="xpath")
        self.elementClick(self.pay, locatorType="xpath")

    def verify_payment_confirmation(self):
        element=self.isElementPresent(self.verify_payment,locatorType="xpath")
        return element

    def verify_amazon_payment_page(self):
        return self.isElementPresent(self.pay_now_amazon, locatorType="xpath")

    def verify_pp_pay_element(self):
        return self.isElementPresent(self.pay, locatorType="xpath")

    def pay_with_cc_dc(self):
        self.elementClick(self.pay_via_justpay,locatorType="xpath")
        time.sleep(variables.WAIT)
        self.sendKeys(variables.CC_NUMBER, self.card_number, locatorType="xpath")
        self.sendKeys(variables.EXPIREY_DATE, self.expiry_date, locatorType="xpath")
        self.sendKeys(variables.CVV, self.cvv_number, locatorType="xpath")
        self.sendKeys(variables.USER_NAME, self.user_name, locatorType="xpath")
        self.sendKeys(variables.MOVIEPASS_USER_EMAIL, self.user_email, locatorType="xpath")
        self.sendKeys(variables.MOBILE_NUMBER, self.user_mobile, locatorType="xpath")
        self.elementClick(self.make_payment, locatorType="xpath")
        time.sleep(variables.WAIT)
        self.sendKeys(variables.CC_PIN, self.cc_pin, locatorType="id")
        self.elementClick(self.cc_submit, locatorType="id")
        time.sleep(variables.WAIT)

    def verify_booking_confirmation(self):
        element = self.isElementPresent(self.verify_ticket_booking, locatorType="xpath")
        return element

    def pay_later_by_simpl(self):
        self.elementClick(self.pay_with_simpl, locatorType="xpath")
        time.sleep(variables.WAIT)
        if self.isElementPresent(self.link_account_simpl, locatorType="xpath"):
            assert False
        else:
            self.elementClick(self.pay_later, locatorType="xpath")

    def phone_pay_guest_payment(self):
        self.elementClick(self.pay_via_phonepay, locatorType="xpath")
        self.sendKeys(variables.USER_NAME, self.name_for_ticket_detail, locatorType="xpath")
        self.sendKeys(variables.USER_EMAIL, self.email_for_ticket_detail, locatorType="xpath")
        self.sendKeys(variables.MOBILE_NUMBER, self.mobile_for_ticket_details, locatorType="xpath")
        self.elementClick(self.make_payment, locatorType="xpath")
        time.sleep(variables.WAIT)
        if self.verify_pp_pay_element():
            self.elementClick(self.pay, locatorType="xpath")
        else:
            self.elementClick(self.use_pp_password, locatorType="id")
            time.sleep(variables.WAIT)
            self.sendKeys(variables.PHONE_PAY_PASS, self.phone_pay_pin, locatorType="id")
            self.elementClick(self.pp_login, locatorType="id")
            time.sleep(variables.WAIT)
            self.elementClick(self.pay, locatorType="xpath")
            time.sleep(variables.WAIT)

    def pay_with_amazon(self):
        self.elementClick(self.amazon_pay, locatorType="xpath")
        time.sleep(variables.WAIT)
        self.sendKeys(variables.USER_NAME, self.name_for_ticket_detail, locatorType="xpath")
        self.sendKeys(variables.USER_EMAIL, self.email_for_ticket_detail, locatorType="xpath")
        self.sendKeys(variables.MOBILE_NUMBER, self.mobile_for_ticket_details, locatorType="xpath")
        self.elementClick(self.make_payment, locatorType="xpath")
        time.sleep(variables.WAIT)
        if self.verify_amazon_payment_page():
            self.elementClick(self.pay_now_amazon, locatorType="xpath")
            time.sleep(variables.WAIT)
        else:
            self.sendKeys(variables.AMAZON_USER, self.amazon_user, locatorType="id")
            self.sendKeys(variables.AMAZON_PASSWORD, self.amazon_passwprd, locatorType="id")
            self.elementClick(self.amazon_singin, locatorType="id")
            time.sleep(variables.WAIT)
            self.elementClick(self.pay_now_amazon, locatorType="xpath")
            time.sleep(variables.WAIT)
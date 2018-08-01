from UtilityPackage.SeleniumDriver import SeleniumDriver
import UtilityPackage.CustomLogger as cl
import logging

"""
LoginToJT class : Page class which contains all the methods and variables. 
All the methods can be re-used by creating object of this class and calling as object.method()
to execute the test case.
Methods defined here are used in TestClass to validate the github login functionality.
"""


class LoginToJT(SeleniumDriver):

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        #super().__init__(driver)
        self.driver = driver

    #Locators in login page for JT              Locator types for reference

    _LoginLink = "//*/span[contains(text(),'Sign In')]"              #xpath
    _EmailField = "contact"                     #id
    _VerifyContact = "contact_verify"           #id
    _PasswordField = "password"                 #id
    _SignInButton = "signin_btn"                #id
    _VerifyLogin = "//*[contains(text(),'My Account')]"            #xpath
    _SignOut = "//*/span[contains(text(),'Sign Out')]"

    def ClickLoginLink(self):
        self.elementClick(self._LoginLink, locatorType="xpath")

    def FillEmailField(self, email):
        self.sendKeys(email, self._EmailField, locatorType="id")

    def VerifyContact(self):
        self.elementClick(self._VerifyContact, locatorType="id")

    def FillPasswordField(self, password):
        self.sendKeys(password, self._PasswordField, locatorType="id")

    def ClickSignInbutton(self):
        self.elementClick(self._SignInButton, locatorType="id")

    def VerifyLogin(self):
        element = self.isElementPresent(self._VerifyLogin, locatorType="xpath")
        return element

    def UserLogin(self, email, password):
        main_window_handle = None
        while not main_window_handle:
            main_window_handle = self.driver.current_window_handle
        self.ClickLoginLink()
        signin_window_handle = None
        while not signin_window_handle:
            for handle in self.driver.window_handles:
                if handle != main_window_handle:
                    signin_window_handle = handle
                    break
        try:
            self.driver.switch_to.window(signin_window_handle)
            self.log.info("Entering the MoviePass User name")
            self.FillEmailField(email)
            self.log.info("Verifying the MoviePass User name")
            self.VerifyContact()
            self.FillPasswordField(password)
            self.log.info("Sigin to JT via Movie Pass user")
            self.ClickSignInbutton()
            self.driver.switch_to.window(main_window_handle)
            self.driver.implicitly_wait(10)
        except:
            self.log.error("Error Occured while Singin to JT")

    def signout_feature(self):
        try:
            self.log.info("Signing out from JT")
            self.elementClick(self._SignOut,locatorType="xpath")
        except:
            self.log.error("Unable to sign out from JT")
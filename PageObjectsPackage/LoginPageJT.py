from UtilityPackage.SeleniumDriver import SeleniumDriver
import UtilityPackage.CustomLogger as cl
import logging,json

"""
LoginToJT class : Page class which contains all the methods and variables. 
All the methods can be re-used by creating object of this class and calling as object.method()
to execute the test case.
Methods defined here are used in TestClass to validate the github login functionality.
"""


class LoginToJT(SeleniumDriver):

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver, locator):
        #super().__init__(driver)
        self.driver = driver
        with open(locator) as f:
            data = json.load(f)
        self.locator = data

    def ClickLoginLink(self):
        self.elementClick(self.locator["_LoginLink"]["xpath"], locatorType="xpath")

    def FillEmailField(self, email):
        self.sendKeys(email, self.locator["_EmailField"]["id"], locatorType="id")

    def VerifyContact(self):
        self.elementClick(self.locator["_VerifyContact"]["id"], locatorType="id")

    def FillPasswordField(self, password):
        self.sendKeys(password, self.locator["_PasswordField"]["id"], locatorType="id")

    def ClickSignInbutton(self):
        self.elementClick(self.locator["_SignInButton"]["id"], locatorType="id")

    def VerifyLogin(self):
        element = self.isElementPresent(self.locator["_VerifyLogin"]["xpath"], locatorType="xpath")
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
            self.elementClick(self.locator["_SignOut"]["xpath"],locatorType="xpath")
        except:
            self.log.error("Unable to sign out from JT")
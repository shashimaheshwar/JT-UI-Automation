import pytest
import logging
import UtilityPackage.CustomLogger as cl


class AssertionClass():
    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver

    def verify_ticket_booking(self, movie_name):
        pass

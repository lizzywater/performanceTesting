import time

from abc import ABCMeta, abstractmethod
from hamcrest import assert_that
from hamcrest import equal_to
from page_objects import PageObject
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait

import settings

class AbstractBasePage(PageObject):

    __metaclass__ = ABCMeta

    def __init__(self, driver):
        # Don't change the variable name w. it's used by PageObject
        self.w = driver
        self.driver = driver
        assert_that(self.has_loaded(), equal_to(True), self.__class__.__name__ + " is not load!")

    def has_loaded(self):
        try:
            return self.is_target_page()
        except NoSuchElementException:
            return False

    #This function will be implement by sub class
    @abstractmethod
    def is_target_page(self):
        pass

    def is_element_displayed(self, by, value):
        WebDriverWait(self.driver, settings.TIMEOUT).until(lambda driver: driver.find_element(by, value))
        return self.driver.find_element(by, value).is_displayed()

    def wait_until_element_is_found(self, xpath_locator, timeout=settings.TIMEOUT):
        time_waited = 0

        while (True):
            try:
                self.driver.find_element_by_xpath(xpath_locator)
                break
            except Exception as e:
                time.sleep(settings.SEARCH_POLL_TIME)
                time_waited += settings.SEARCH_POLL_TIME
                if time_waited <= timeout:
                    continue
                else:
                    break

    def wait_until_element_is_displayed(self, xpath_locator):
        WebDriverWait(self.driver, settings.TIMEOUT).until(lambda driver: driver.find_element_by_xpath(xpath_locator).is_displayed())

    def wait_until_element_display_status(self, xpath_locator, status):
        time_waited = 0

        while (time_waited < settings.TIMEOUT):
            element = self.driver.find_element_by_xpath(xpath_locator)
            display_status = element.is_displayed()
            if (display_status == status):
                break
            else:
                time.sleep(settings.SEARCH_POLL_TIME)
                time_waited += settings.SEARCH_POLL_TIME

    def wait_until_element_enabled(self, xpath_locator, time_out=settings.TIMEOUT):
        time_waited = 0

        while (time_waited < time_out):

            element = self.driver.find_element_by_xpath(xpath_locator)
            status = element.is_enabled()
            if (status == True):
                break
            else:
                time.sleep(settings.SEARCH_POLL_TIME)
                time_waited += settings.SEARCH_POLL_TIME
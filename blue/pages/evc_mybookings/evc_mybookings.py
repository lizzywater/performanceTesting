import time

from selenium.webdriver.common.by import By
from hamcrest import assert_that
from hamcrest import equal_to

import settings
from ef_common.seleniumhelper import SeleniumHelper
from page_objects import PageElement,MultiPageElement
from pages.abstract_base_page import AbstractBasePage
from tools.login_api import LoginAPI

class EvcMyBookings(AbstractBasePage):

    CURRENT_PAGE_URL = "/evc/mybookings?ctr=cc"
    EVC_ROOM_STRING = ".englishtown.com/evc/room"

    # Partial xpath used to search target element based on found elements.
    TECH_CHECK_BUTTON_XPATH ="div/div/div/button"
    TECH_CHECK_BLOCK_XPATH = "div[2]/div[@class='evc-classinfo-techcheck']"
    CLASS_DATE_XPATH = "div/div[@class='evc-topicandtime']/p"
    CLASS_TOPIC_NAME_XPATH = "div/div[@class='evc-topicandtime']/h4"
    TEACHER_NAME_XPATH = "div[3]/div/div[1]/div[2]"

    # Full xpath used to locate elements directly.
    EVC_MYBOOKINGS_ICON_XPATH = ".//*[@class='evc-mybookings']/div/h4"
    TECH_CHECK_TITLE_XPATH = ".//*[@id='et-content']/div[1]/div[1]/div/div/div[1]/h4"
    ENTER_CLASS_BUTTON_XPATH = ".//*[@id='et-content']/div[2]/div/div[3]/div/div/div[2]/div[3]/div[2]/div[1]/div/div[2]/button"
    BOOK_LESSON_BUTTON_XPATH = ".//*[@id='et-content']/div[2]/div/div[4]/div/div[2]/div[2]/a/button"
    MYBOOKINGS_LOADING_XPATH = "//*[@id='et-content']/div[2]/div/div[2]/img"
    EVC_CLASSINFO_PROPERTIES_XPATH = ".//*[@class='evc-mybookings-list']//div[@class='evc-classinfo-properties clearfix']"
    NEXT_BUTTON_XPATH = ".//*[@id='et-content']/div/div/div/div/div[3]/div/div[2]/button[2]"
    TECH_CHECK_DIALOG_XPATH = ".//*[@id='et-content']/div[1]/div[1]/div/div/div[1]/h4"

    booked_class_js = "return $('.evc-mybookings-list .evc-topicandtime').length"
    pass_tech_check_js = "$('.btn.btn-primary.tck-ui-ft-next').removeClass('tck-disabled')"

    # Page Objects
    evc_mybookings_icon = PageElement(xpath=EVC_MYBOOKINGS_ICON_XPATH)
    book_lesson_button = PageElement(xpath=BOOK_LESSON_BUTTON_XPATH)
    mybookings_loading = PageElement(xpath=MYBOOKINGS_LOADING_XPATH)
    evc_classinfo_properties = MultiPageElement(xpath=EVC_CLASSINFO_PROPERTIES_XPATH)
    class_topic_name = MultiPageElement(xpath=CLASS_TOPIC_NAME_XPATH)
    class_date = MultiPageElement(xpath=CLASS_DATE_XPATH)
    teacher_name = MultiPageElement(xpath=TEACHER_NAME_XPATH)
    next_button = PageElement(xpath=NEXT_BUTTON_XPATH)
    tech_check_dialog = PageElement(xpath=TECH_CHECK_DIALOG_XPATH)
    enter_class_button = PageElement(xpath=ENTER_CLASS_BUTTON_XPATH)

    def __init__(self, driver):
        AbstractBasePage.__init__(self, driver)

    def wait_page_load(self):
        time_index = 0

        while time_index < settings.TIMEOUT:
            try:
                status = self.mybookings_loading.is_displayed()
                if not status:
                    break
            except:
                pass
            time.sleep(settings.SEARCH_POLL_TIME)
            time_index += settings.SEARCH_POLL_TIME

    def is_target_page(self):
        return self.is_element_displayed(By.XPATH, self.EVC_MYBOOKINGS_ICON_XPATH)

    def book_lesson(self):
        self.book_lesson_button.click()

    def get_booked_info(self):
        return self.driver.execute_script(self.booked_class_js)

    def get_class_info(self):
        '''Place holder method, will update after cases schedule & book class cases done.'''
        class_lists = []

        if len(self.evc_classinfo_properties) > 0:
            for booked_class in self.evc_classinfo_properties:
                class_info = {}
                class_info["topic"] = booked_class.find_element_by_xpath(self.CLASS_TOPIC_NAME_XPATH).get_attribute("innerHTML")
                class_info["start_date"] = booked_class.find_element_by_xpath(self.CLASS_DATE_XPATH).text
                class_info["teacher"] = booked_class.find_element_by_xpath(self.TEACHER_NAME_XPATH).text
                class_lists.append(class_info)
        else:
            print "No class booked."

        return class_lists

    def pass_tech_check(self):
        '''Place holder method, will update after cases schedule & book class cases done.'''
        for i in self.evc_classinfo_properties:
            time.sleep(settings.WAIT_PAGE_REFRESH)
            tech_check = i.find_element_by_xpath(self.TECH_CHECK_BLOCK_XPATH)
            value = tech_check.get_attribute("style")

            if value == "display: block;":
                tech_check.find_element_by_xpath(self.TECH_CHECK_BUTTON_XPATH).click()
                self.do_tech_check()

            # After passed tech check, the page will refresh automatically, hence need to wait page reload.
            time.sleep(settings.WAIT_PAGE_REFRESH)

    def do_tech_check(self):
        tech_check_steps = 0

        while tech_check_steps < settings.TECH_CHECK_STEPS:
            self.wait_until_element_is_displayed(self.TECH_CHECK_TITLE_XPATH)
            time.sleep(settings.SEARCH_POLL_TIME)
            self.driver.execute_script(self.pass_tech_check_js)
            self.next_button.click()
            tech_check_steps += settings.SEARCH_POLL_TIME

    def enter_class(self):
        self.wait_until_element_enabled(self.ENTER_CLASS_BUTTON_XPATH,settings.ENTER_CLASS_COUNTDOWN)
        self.wait_until_element_display_status(self.ENTER_CLASS_BUTTON_XPATH, True)
        self.enter_class_button.click()

    def class_url_check(self):
        time_used = 0
        while time_used < settings.TIMEOUT:
            url = self.driver.current_url
            if self.EVC_ROOM_STRING in url:
                return True
            else:
                time.sleep(settings.URL_CHECK_INTERVAL)
                time_used += settings.URL_CHECK_INTERVAL

        return False

if __name__ == "__main__":

    login = LoginAPI()
    target_url = settings.DOMAIN + EvcMyBookings.CURRENT_PAGE_URL
    account_dict = settings.Account.B2B_Account
    browser = SeleniumHelper.open_browser()
    login.page_login(browser, target_url, account_dict)

    evc_mybookings = EvcMyBookings(browser)
    evc_mybookings.wait_page_load()
    evc_mybookings.get_booked_info()
    evc_mybookings.get_class_info()
    evc_mybookings.pass_tech_check()
    evc_mybookings.enter_class()

    assert_that(evc_mybookings.class_url_check(), equal_to(True))
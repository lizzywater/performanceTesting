from abstract_base_page import AbstractBasePage
from school_pages.home_page import  HomePage
from page_objects import PageElement
from selenium.webdriver.common.by import By
import settings

class LoginPage(AbstractBasePage):

    user_name_textbox = PageElement(xpath="//input[@id='UserName']")
    password_textbox = PageElement(xpath="//input[@id='Password']")
    login_button = PageElement(xpath="//a[@class='et-btn-submit']")

    def __init__(self, driver):
        AbstractBasePage.__init__(self, driver)

    def is_target_page(self):
        return self.is_element_displayed(By.XPATH, "//input[@id='UserName']")

    def set_user_name(self, user_name):
        self.user_name_textbox.clear()
        self.user_name_textbox.send_keys(user_name)

    def set_password(self, password):
        self.password_textbox.clear()
        self.password_textbox.send_keys(password)

    def click_login_button(self):
        self.login_button.click()

    def do_login(self, user_name, password, return_page=None):

        """
        do_login and return specific page
        :param user_name:
        :param password:
        :param return_page: page class
        :return:
        """

        self.set_user_name(user_name)
        self.set_password(password)
        self.click_login_button()

        if return_page == None:
            return HomePage(self.driver)
        else:
            self.driver.get(settings.DOMAIN + return_page.url)
            return return_page(self.driver)
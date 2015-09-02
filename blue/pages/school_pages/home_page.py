from selenium.webdriver.common.by import By
from abstract_base_school_page import AbstractBaseSchoolPage

class HomePage(AbstractBaseSchoolPage):

    url = '/campus/mypage/home'

    def __init__(self, driver):
        AbstractBaseSchoolPage.__init__(self, driver)

    def is_target_page(self):
        return self.is_element_displayed(By.XPATH, "//ul[@class='lesson-navigator in out']")
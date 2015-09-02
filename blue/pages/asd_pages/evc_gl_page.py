from pages.asd_pages.abstract_base_asd_page import AbstractBaseASDPage
from selenium.webdriver.common.by import By
from page_objects import PageElement

class EvcGLPage(AbstractBaseASDPage):

    url = '/evc/gl'

    weekly_schedule_dropdown = PageElement(xpath="//div[@id='evc-hook-weekly-topic']/div/button")

    def __init__(self, driver):
        AbstractBaseASDPage.__init__(self, driver)

    def is_target_page(self):
        return self.is_element_displayed(By.XPATH, "//div[@id='evc-hook-weekly-topic']")

    def click_weekly_schedule_dropdown(self):
        self.weekly_schedule_dropdown.click()
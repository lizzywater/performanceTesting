from abstract_base_page import AbstractBasePage
from page_objects import PageElement

class PageHeader(AbstractBasePage):

    home_icon = PageElement(xpath="//img[ends-with(@src, 'logo_ef_v2.png')]")

    def __init__(self, driver):
        AbstractBasePage.__init__(self, driver)

    def is_target_page(self):
        return True


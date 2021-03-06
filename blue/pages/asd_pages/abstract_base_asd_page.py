from abc import ABCMeta
from pages.abstract_base_page import AbstractBasePage

class AbstractBaseASDPage(AbstractBasePage):

    __metaclass__ = ABCMeta

    def __init__(self, driver):
        AbstractBasePage.__init__(self, driver)
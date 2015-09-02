import settings

from hamcrest import assert_that
from hamcrest import equal_to

from ef_common.frontend_testcase import FrontEndTestCase
from ef_common.take_screenshot import take_screenshot
from pages.evc_mybookings.evc_mybookings import EvcMyBookings

from tools.login_api import LoginAPI

class TestEvcMyBookings(FrontEndTestCase):

    @take_screenshot
    def runTest(self):
        login = LoginAPI()
        target_url = settings.DOMAIN + EvcMyBookings.CURRENT_PAGE_URL
        account_dict = settings.Account.B2B_Account
        login.page_login(self.browser, target_url, account_dict)

        evc_mybookings = EvcMyBookings(self.browser)
        evc_mybookings.wait_page_load()
        evc_mybookings.get_booked_info()
        evc_mybookings.get_class_info()
        evc_mybookings.pass_tech_check()
        evc_mybookings.enter_class()

        assert_that(evc_mybookings.class_url_check(), equal_to(True))
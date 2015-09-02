from ef_common.frontend_testcase import FrontEndTestCase
from ef_common.take_screenshot import take_screenshot
from pages.login_page import LoginPage
from pages.school_pages.home_page import HomePage
from pages.asd_pages.evc_gl_page import EvcGLPage
import settings

class TestLogin(FrontEndTestCase):

    @take_screenshot
    def runTest(self):
        self.browser.get(settings.COMMON_LOGIN_URL)
        login_page = LoginPage(self.browser)
        evc_gl_page = login_page.do_login(settings.Account.B2B_Account.get("username"),settings.Account.B2B_Account.get("password"), return_page=EvcGLPage)
        evc_gl_page.click_weekly_schedule_dropdown()

if __name__ == "__main__":
     test = TestLogin()
     test.create_browser_driver()
     test.browser.get(settings.COMMON_LOGIN_URL)
     test.runTest()
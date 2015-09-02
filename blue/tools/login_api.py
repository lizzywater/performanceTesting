import requests

import settings
from ef_common.seleniumhelper import SeleniumHelper

class LoginAPI(object):

    def __init__(self):
        self.s = requests.session()

    def cookie_to_selenium_format(self, cookie):
        cookie_selenium_mapping = {'path':'', 'secure':'', 'name':'', 'value':'','expires':''}
        cookie_dict = {}
        if getattr(cookie, 'domain_initial_dot'):
            cookie_dict['domain'] = '.' + getattr(cookie, 'domain')
        else:
            cookie_dict['domain'] = getattr(cookie, 'domain')
        for k in cookie_selenium_mapping.keys():
            key = k
            value = getattr(cookie, k)
            cookie_dict[key] = value
        return cookie_dict

    def page_login(self, driver, target_url, account_dict):
        login_url = settings.COOKIE_LOGIN_URL
        login_status = self.s.post(login_url, account_dict)
        if int(login_status.status_code) == 200:
            all_cookies = tuple(self.s.cookies)
            driver.get(target_url)
            driver.delete_all_cookies()
            for i in range(len(all_cookies)):
                driver.add_cookie(self.cookie_to_selenium_format(all_cookies[i]))
            driver.get(target_url)
        else:
            raise ValueError, "Response code not equal to 200, log in failed!"

if __name__ == "__main__":

    login = LoginAPI()
    target_url = settings.MY_BOOKINGS_PAGE_URL
    account_dict = settings.Account.B2B_Account
    driver = SeleniumHelper.open_browser()
    login.page_login(driver, target_url, account_dict)
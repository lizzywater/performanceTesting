import os

from tools.property_utils import PropertyUtils
from tools.file_utils import FileUtils
from settings.environment import Environment, UAT_Account, QA_Account, STG_Account

property_utils = PropertyUtils(FileUtils.get_current_file_path(__file__) + os.path.sep + "temp.conf")
environment = property_utils.get_property_value("ENV")

if environment == '':
    environment = Environment.UAT

environment = Environment.UAT

DOMAIN = "http://%s.englishtown.com" % environment
COMMON_LOGIN_URL =  DOMAIN + "/login.aspx?ctr=us"
COOKIE_LOGIN_URL = DOMAIN + "/login/handler.ashx"
MY_BOOKINGS_PAGE_URL = DOMAIN + "/school/evc/pl"
PL_TIME_SLOTS_URL = "http://%s.englishtown.com/school/evc/pl/slots" % environment
PL_TIME_SLOTS = {'TimeZone_id':'Eastern Standard Time', 'SubserviceType':'', 'HasBilingual':'true',\
        'Gender':'', 'BaseDate':'', 'DayOffset':'0', 'DayCount':'7'}
AVAILABLE_PL_URL = "http://%s.englishtown.com/school/evc/pl/available" % environment
BOOKED_PL_URL = "http://%s.englishtown.com/school/evc/pl/booked" % environment
STUDENT_CONTEXT_QUERY_STRING_URL = \
    "http://%s.englishtown.com/services/shared/queryproxy?c=countrycode=cn|culturecode=en|partnercode=Corp|siteversion=development" \
    % environment
PL_BOOK_URL = "http://%s.englishtown.com/school/evc/pl/book" % environment
PL_UPDATE_TOPIC_URL = "http://%s.englishtown.com/school/evc/pl/updatetopic" % environment
STUDENT_CONTEXT_QUERY_STRING = {'q':'evc_context!current|evc_studentcourse!current'}
MAXIMUM_ALLOWED_CLASSES_NUMBER = 4

# set Test Case Timeout as 600 seconds
TESTCASE_TIMEOUT = 600

TIMEOUT = 60

ENTER_CLASS_COUNTDOWN = 1200

TECH_CHECK_STEPS = 3

WAIT_PAGE_REFRESH = 5

URL_CHECK_INTERVAL = 5

# control re_run function, default is True
RE_RUN_FLAG = False

# if debug test cases locally then keep the browser active after execution done. Default value is False
DEBUG_RUN = False

# set queue_size as 10 means that there are at most 10 test cases can be executed concurrently
QUEUE_SIZE = 1

SEARCH_POLL_TIME = 1

FIREFOX_BINARY = None
FIREFOX_PROFILE = None

# initialize user account
if environment == Environment.UAT:
    Account = UAT_Account
elif environment == Environment.QA:
    Account = QA_Account
elif environment == Environment.STAGING:
    Account = STG_Account

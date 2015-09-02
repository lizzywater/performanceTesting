import requests
from hamcrest import assert_that
from hamcrest import equal_to

import settings

class BookPL():

    def __init__(self):
        self.__s = requests.session()

    def get_login_status(self, account_dict):
        log_in = self.send_post_request(settings.COOKIE_LOGIN_URL, account_dict)
        if log_in.status_code == 200:
            return True
        else:
            return False

    def send_post_request(self, target_url, data_to_send):
        return self.__s.post(target_url, data_to_send)

    def get_available_pl_slots(self):
        available_pl = self.send_post_request(settings.PL_TIME_SLOTS_URL,settings.PL_TIME_SLOTS)
        return available_pl.json()['Slots']

    def get_available_classes(self):
        available_list =[]
        json_data = self.get_available_pl_slots()
        for data in range(len(json_data)):
            if json_data[data]['Status'] == "A":
                available_list.append(json_data[data])

        return available_list

    def get_info_of_booked_classes(self):
        previous_booked_data = pl_book.send_post_request(settings.BOOKED_PL_URL, pl_book.get_post_data_for_booked_class())
        previous_booked_classes = self.get_booked_classes_detail_info(previous_booked_data.json()['MyBookings'])
        return previous_booked_classes

    def generate_class_post_data(self, returned_student_course_info):
        # Parameter key used for post
        target_parameters = ['member_id', 'languageCode', 'partnerCode', 'marketCode', 'tokenTime', \
                             'token', 'schoolVersion', 'studentCourse_id', 'course_id', 'courseUnit_id']
        post_dict = self.return_specific_dict_from_given_dict(target_parameters, returned_student_course_info)
        post_dict['IsVideo'] = 'false'
        post_dict['Teacher_id'] = '0'
        post_dict['SubserviceType'] = ''
        post_dict['Gender'] = ''
        post_dict['Flow'] = ''

        return post_dict

    def update_class_topic(self, *json_data):
        # Parameter key used for post
        target_parameters = ['Member_id', 'Class_id', 'TokenTime', 'Token']
        dict = self.return_specific_dict_from_given_dict(target_parameters, json_data)
        dict['Topic_id'] = '1'

        return dict

    def book_pl(self, available_classes, number_of_class_to_book):
        class_student_info_list = []
        number_of_booked_classes = len(self.get_info_of_booked_classes())
        remain_number = settings.MAXIMUM_ALLOWED_CLASSES_NUMBER - number_of_booked_classes

        # The business logic requires the maximum number of booked classes should not exceed 4.
        if not 0 < number_of_class_to_book <= remain_number <= len(available_classes):
            print "Currently there are --%d-- of available classes." % len(available_classes)
            print "The Maximum number of classes student can book is 4."
            print "Now the student already booked --%d-- class(es)." % number_of_booked_classes
            raise ValueError, "Book number must meet above requirements, please re-run."

        for i in range(0, number_of_class_to_book):
            class_student_info = {}

            pl_start_time = self.send_post_request(settings.AVAILABLE_PL_URL, available_classes[i])
            class_student_info['StartTime'] = pl_start_time.json()['StartTime']

            get_student_course_info = self.query_student_course_info()
            # Compose all of the data which is necessary to book a class.
            pl_book_data = self.generate_class_post_data(get_student_course_info.json())
            pl_book_data['StartTime'] = available_classes[i]['StartTime']
            pl_book_data['EndTime'] = available_classes[i]['EndTime']

            book_results = self.send_post_request(settings.PL_BOOK_URL, pl_book_data)

            if book_results.status_code == 200:
                # Update class type, class name to finish book process.
                update_class_info = self.update_class_topic(pl_book_data,book_results.json())
                self.send_post_request(settings.PL_UPDATE_TOPIC_URL, update_class_info)
                class_student_info['Class_id'] = update_class_info['Class_id']
                class_student_info['Topic_id'] = update_class_info['Topic_id']
                class_student_info['Member_id'] = update_class_info['Member_id']
                class_student_info_list.append(class_student_info)

        return class_student_info_list

    def get_post_data_for_booked_class(self):
        booked_dict = {}

        book_data = self.generate_class_post_data(self.query_student_course_info().json())
        booked_dict['Student_id'] = book_data['Member_id']
        booked_dict['Timezome_id'] = settings.PL_TIME_SLOTS['TimeZone_id']
        booked_dict['MarketCode'] = book_data['MarketCode']
        booked_dict['PartnerCode'] = book_data['PartnerCode']
        booked_dict['Token'] = book_data['Token']
        booked_dict['TokenTime'] = book_data['TokenTime']

        return booked_dict

    def query_student_course_info(self):
        return self.send_post_request(settings.STUDENT_CONTEXT_QUERY_STRING_URL,settings.STUDENT_CONTEXT_QUERY_STRING)

    def get_new_booked_classes(self, previous_booked_classes, all_booked_classes):
        new_booked_classes = []

        for class_info in all_booked_classes:
                if class_info not in previous_booked_classes:
                    new_booked_classes.append(class_info)

        return new_booked_classes

    def get_booked_classes_detail_info(self, class_raw_data):
        class_detail_info_list = []
        # Parameter key used for post
        target_parameters = ['Topic', 'TeacherName', 'SubserviceType', 'Class_id', 'ClassTypeCode', 'IsBilingual', \
                             'IsVideo', 'Duration_Minutes', 'StartTime', 'Topic_id']

        for class_info in class_raw_data:
            class_detail_info = {}
            for key in class_info:
                if key in target_parameters:
                    class_detail_info[key] = class_info[key]
                    continue
            class_detail_info_list.append(class_detail_info)

        return class_detail_info_list

    def capitalize_first_character(self, argument):
        return argument.capitalize()[0] + argument[1:]

    def return_specific_dict_from_given_dict(self, specific_list, input_data):
        post_dict = {}
        for info in input_data:
            for key in info.keys():
                if key in specific_list:
                    capitalized_key = self.capitalize_first_character(key)
                    post_dict[capitalized_key] = info[key]
                    continue
        return post_dict

if __name__ == "__main__":

    pl_book = BookPL()
    assert_that(pl_book.get_login_status(settings.Account.B2C_Account), equal_to(True))

    # Get the available PL classes.
    available_pl_classes = pl_book.get_available_classes()
    booked_classes = pl_book.get_info_of_booked_classes()
    print "The classes already exists are: \n %s" % booked_classes

    # Book PL classes
    pl_book.book_pl(available_pl_classes,1)
    class_raw_data = pl_book.send_post_request(settings.BOOKED_PL_URL, pl_book.get_post_data_for_booked_class())
    all_booked_classes = pl_book.get_booked_classes_detail_info(class_raw_data.json()['MyBookings'])

    # If success, print out the booked class info to console for later use.
    new_booked_classes = pl_book.get_new_booked_classes(booked_classes, all_booked_classes)
    print "The new booked class info are: \n %s" % new_booked_classes
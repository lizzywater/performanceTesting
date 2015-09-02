import os

class PropertyUtils:

    def __init__(self, file_name):
        with open(file_name, 'r') as f:
            self.lst_file_content = f.readlines()

    def get_property_value(self, key):
        for line in self.lst_file_content:
            curr_key = line.split('=')[0]
            curr_value = line.split('=')[1]
            if curr_key == key:
                return curr_value

        return ""

if __name__ == '__main__':
    property_utils = PropertyUtils(os.path.dirname(__file__) + os.path.sep + ".." + os.path.sep + "settings/temp.conf")
    print property_utils.get_property_value("ENV")
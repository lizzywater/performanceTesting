import os

class FileUtils(object):

    @classmethod
    def get_current_file_path(self, file):
        return os.path.split(os.path.realpath(file))[0]


if __name__ == '__main__':
    print FileUtils.get_current_file_path(__file__);
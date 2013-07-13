import datetime
import time


def create_dir_name():
    return "dir" + str(time.mktime(datetime.datetime.now().timetuple()))

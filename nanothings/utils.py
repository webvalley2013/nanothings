from time import time
from os.path import join as j


def create_dir_name(path):
    p = j(path, str(int(time()*1000)))
    return p

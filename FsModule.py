import os


def get_root_path():
    path_list = os.path.realpath(__file__).split("\\")
    return '\\'.join(path_list[:len(path_list) - 1], )

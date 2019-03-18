from os import listdir
from os.path import isfile, join, realpath


class Constants:
    def __init__(self):
        self.__path_list = realpath(__file__).split("\\")
        self.ROOT_PATH = '\\'.join(self.__path_list[:len(self.__path_list) - 1], )

        self.DIR_TO_LOOK_IN = self.ROOT_PATH + "\\test_events\\"
        self.DIR_TO_SAVE_IN = self.ROOT_PATH + "\\generated_csvs\\"
        self.FILE_LIST = [file for file in listdir(self.DIR_TO_LOOK_IN) if isfile(join(self.DIR_TO_LOOK_IN, file))]

        self.COLUMN_LIST = [
            "$COLUMNS$MASCH_NR",
            "BEGIN_ZEIT",
            "BEGIN_DAT",
            "ENDE_ZEIT",
        ]

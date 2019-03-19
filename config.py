from os import listdir
from os.path import isfile, join, realpath


class Constants:
    def __init__(self):
        self.__PATH_LIST = realpath(__file__).split("\\")
        self.PATH_ROOT = '\\'.join(self.__PATH_LIST[:len(self.__PATH_LIST) - 1], )

        self.DIR_BASE_FILES = join(self.PATH_ROOT, "test_events")
        self.DIR_GENERATED_FILES = join(self.PATH_ROOT, "generated_csvs")
        self.FILE_LIST = [file for file in listdir(self.DIR_BASE_FILES) if isfile(join(self.DIR_BASE_FILES, file))]

        self.COLUMN_LIST = [
            "$COLUMNS$MASCH_NR",
            "BEGIN_ZEIT",
            "BEGIN_DAT",
            "ENDE_ZEIT",
        ]

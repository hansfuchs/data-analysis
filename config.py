from os.path import join, realpath


class Constants:
    def __init__(self):
        self.__PATH_LIST = realpath(__file__).split("\\")
        self.PATH_ROOT = '\\'.join(self.__PATH_LIST[:len(self.__PATH_LIST) - 1], )

        self.DIR_BASE_FILES = join(self.PATH_ROOT, "test_events")
        self.DIR_PREPARED_CSVS = join(self.PATH_ROOT, "prepared_csvs")
        self.DIR_MACHINE_CSVS = join(self.PATH_ROOT, "machine_csvs")

        self.COLUMN_LIST = [
            "$COLUMNS$MASCH_NR",
            "BEGIN_ZEIT",
            "BEGIN_DAT",
            "ENDE_ZEIT",
            #"STOER_TEXT"
        ]
        self.COLUMN_NAME_OF_MACHINE_NR = "$COLUMNS$MASCH_NR"

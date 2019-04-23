from os.path import join, realpath
from typing import List


class Constants:
    def __init__(self):
        self.__PATH_LIST: str = realpath(__file__).split("\\")
        self.PATH_ROOT: str = '\\'.join(self.__PATH_LIST[:len(self.__PATH_LIST) - 1], )

        self.DIR_BASE_FILES: str = join(self.PATH_ROOT, "events")
        self.DIR_PREPARED_CSVS: str = join(self.PATH_ROOT, "prepared_csvs")
        self.DIR_MACHINE_SERIES_CSVS: str = join(self.PATH_ROOT, "machine_series_csvs")
        self.DIR_MACHINE_CSVS: str = join(self.PATH_ROOT, "machine_csvs")
        self.DIR_PLOTS: str = join(self.PATH_ROOT, 'plots')

        self.COL_LIST: List[str] = [
            "$COLUMNS$MASCH_NR",
            "BEGIN_ZEIT",
            "ENDE_ZEIT",
            "BEGIN_DAT",
            "STOERTXT_NR"
        ]
        self.COL_MACHINE_NR: str = "$COLUMNS$MASCH_NR"
        self.COL_DATE: str = "BEGIN_DAT"
        self.COL_TIME: str = "BEGIN_ZEIT"
        self.COL_STATUS_CODE: str = "STOERTXT_NR"
        self.ALLOWED_STATUS_CODES: List[int] = list(range(1, 14))

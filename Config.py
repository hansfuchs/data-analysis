import multiprocessing as mp
from os.path import join, realpath
from typing import List


class Config:
    def __init__(self):
        self.__PATH_LIST: str = realpath(__file__).split("\\")
        self.PATH_ROOT: str = '\\'.join(self.__PATH_LIST[:len(self.__PATH_LIST) - 1], )

        self.DIR_BASE_FILES: str = join(self.PATH_ROOT, "events")
        self.DIR_PREPARED_CSVS: str = join(self.PATH_ROOT, "prepared_csvs")
        self.DIR_MACHINE_SERIES_CSVS: str = join(self.PATH_ROOT, "machine_series_csvs")
        self.DIR_MACHINE_CSVS: str = join(self.PATH_ROOT, "machine_csvs")
        self.DIR_PLOTS: str = join(self.PATH_ROOT, 'plots')
        self.DIR_DATA_GAPS: str = join(self.PATH_ROOT, 'data_gaps')

        self.FILE_UNIQUE_MACHINES: str = 'unique_machines.txt'
        self.FILE_LOGGER: str = 'log.txt'
        self.FILE_DATA_GAPS: str = 'data_gaps.csv'
        self.FILE_DATA_GAPS_BY_PREV: str = 'data_gaps_by_prev_state.csv'
        self.FILE_DATA_GAPS_BY_NEXT: str = 'data_gaps_by_next_state.csv'
        self.FILE_DATA_GAPS_BY_PREV_AND_NEXT: str = 'data_gaps_by_prev_and_next_state.csv'

        self.UNIQUE_MACHINES: List[str] = []
        with open(self.FILE_UNIQUE_MACHINES, 'r+') as file:
            self.UNIQUE_MACHINES = file.read().split(',')

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

        self.CPU_COUNT: int = mp.cpu_count()

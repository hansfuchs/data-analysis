import datetime
from os import mkdir
from os.path import join, exists

import pandas as pd
from typing import List, Dict, Set

from Config import Config
from utils import get_files_of_dir, string_to_date2


class DataGapClassifier:

    conf: Config = Config()

    def __init__(
            self,
            start_date: str,
            num_of_days: int,
            gap_threshold: int = 1
    ):
        self.machine_csvs: List[str] = get_files_of_dir(self.conf.DIR_MACHINE_CSVS)

        self.start_date: datetime.datetime = string_to_date2(start_date)
        self.dates_as_date: List[datetime.datetime] = [
            self.start_date + datetime.timedelta(days=x) for x in range(0, num_of_days)
        ]
        self.dates_as_date = sorted(self.dates_as_date)
        self.dates: List[str] = [date.strftime('%Y-%m-%d') for date in self.dates_as_date]

        self.num_of_days: int = num_of_days
        self.gap_threshold: int = gap_threshold

        if not exists(self.conf.DIR_DATA_GAPS):
            mkdir(self.conf.DIR_DATA_GAPS)
        self.data_gap_file: str = join(
            self.conf.PATH_ROOT,
            self.conf.DIR_DATA_GAPS,
            self.conf.FILE_DATA_GAPS
        )

    def extract_data_gaps(self):
        data_dict: Dict[str, List[any]] = {
            'MACHINE_NR': [],
            'BEGIN_DATE': [],
            'END_DATE': [],
            'PREV_STATE': [],
            'NEXT_STATE': []
        }
        for file in self.machine_csvs:     # type: str
            df: pd.DataFrame = pd.read_csv(
                join(self.conf.DIR_MACHINE_CSVS, file),
                sep=',',
                low_memory=False
            )

            missing_days: List[str] = []
            for date in self.dates:     # type: str
                if date not in df[self.conf.COL_DATE].unique():
                    missing_days.append(date)

            for day in missing_days:    # type: str
                # check whether day is inside an already documented time range and continue if True
                machine_nrs: Set[str] = set(data_dict['MACHINE_NR'])
                already_checked_days: Dict[str, List[str]] = {}
                for machine in machine_nrs:
                    already_checked_days[machine] = []

                for index in range(0, len(data_dict['BEGIN_DATE'])):
                    curr_machine: str = data_dict['MACHINE_NR'][index]
                    curr_day: datetime.datetime = string_to_date2(data_dict['BEGIN_DATE'][index])
                    end_day: datetime.datetime = string_to_date2(data_dict['END_DATE'][index])

                    already_checked_days[curr_machine].append(curr_day.strftime('%Y-%m-%d'))
                    while curr_day != end_day:
                        curr_day += datetime.timedelta(days=1)
                        already_checked_days[curr_machine].append(curr_day.strftime('%Y-%m-%d'))

                day_already_checked: bool = False
                for machine, days in already_checked_days.items():
                    if machine == df[self.conf.COL_MACHINE_NR].values[0] and day in already_checked_days[machine]:
                        day_already_checked = True

                if day_already_checked:
                    continue

                data_dict['MACHINE_NR'].append(df[self.conf.COL_MACHINE_NR].values[0])
                data_dict['BEGIN_DATE'].append(day)

                end_date: datetime.datetime = string_to_date2(day)
                while True:
                    if (end_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d') in missing_days:
                        end_date += datetime.timedelta(days=1)
                    else:
                        break
                data_dict['END_DATE'].append(end_date.strftime('%Y-%m-%d'))

                prev_day: datetime.datetime = string_to_date2(day) - datetime.timedelta(days=1)
                prev_day_str: str = prev_day.strftime('%Y-%m-%d')
                if prev_day_str in df[self.conf.COL_DATE].unique():
                    temp_df: pd.DataFrame = df.loc[df[self.conf.COL_DATE] == prev_day_str]
                    data_dict['PREV_STATE'].append(temp_df.tail(1)[self.conf.COL_STATUS_CODE].values[0])

                next_day: datetime.datetime = end_date + datetime.timedelta(days=1)
                temp_df: pd.DataFrame = df.loc[df[self.conf.COL_DATE] == next_day.strftime('%Y-%m-%d')]
                data_dict['NEXT_STATE'].append(temp_df.head(1)[self.conf.COL_STATUS_CODE].values[0])

        with open(join(self.conf.DIR_DATA_GAPS, self.conf.FILE_DATA_GAPS), "w+") as out_file:
            out_file.write(pd.DataFrame(data=data_dict).to_csv())

    def group_by_prev_state(self, df: pd.DataFrame):
        df = df.sort_values(by='PREV_STATE')
        with open(join(
                self.conf.DIR_DATA_GAPS,
                self.conf.FILE_DATA_GAPS.replace('.', '_by_prev_state.')
            ),
            'w+'
        ) as f:
            f.write(df.to_csv())

    def group_by_next_state(self, df: pd.DataFrame):
        df = df.sort_values(by='NEXT_STATE')
        with open(
            join(
                self.conf.DIR_DATA_GAPS,
                self.conf.FILE_DATA_GAPS.replace('.', '_by_next_state.')
            ),
            'w+'
        ) as f:
            f.write(df.to_csv())

    def group_by_prev_and_next_state(self, df: pd.DataFrame):
        df = df.sort_values(by=['PREV_STATE', 'NEXT_STATE'])
        with open(join(
                self.conf.DIR_DATA_GAPS,
                self.conf.FILE_DATA_GAPS.replace('.', '_by_prev_and_next_state.')
            ),
            'w+'
        ) as f:
            f.write(df.to_csv())

    def group_gaps(self):
        df: pd.DataFrame = pd.read_csv(
            join(self.conf.DIR_MACHINE_CSVS, self.data_gap_file),
            sep=',',
            low_memory=False
        )
        self.group_by_prev_state(df)
        self.group_by_next_state(df)
        self.group_by_prev_and_next_state(df)

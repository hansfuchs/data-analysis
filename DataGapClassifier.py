import datetime
from os import mkdir
from os.path import join, exists

import pandas as pd
from typing import List, Dict

from config import Constants
from utils import get_files_of_dir, string_to_date2


class DataGapClassifier:

    const: Constants = Constants()

    def __init__(
            self,
            start_date: str,
            num_of_days: int,
            gap_threshold: int = 1
    ):
        self.files: List[str] = get_files_of_dir(self.const.DIR_MACHINE_CSVS)

        self.start_date: datetime.datetime = string_to_date2(start_date)
        self.dates_as_date: List[datetime.datetime] = [
            self.start_date + datetime.timedelta(days=x) for x in range(0, num_of_days)
        ]
        self.dates_as_date = sorted(self.dates_as_date)
        self.dates: List[str] = [date.strftime('%Y-%m-%d') for date in self.dates_as_date]

        self.num_of_days: int = num_of_days
        self.gap_threshold: int = gap_threshold

        if not exists(self.const.DIR_DATA_GAPS):
            mkdir(self.const.DIR_DATA_GAPS)

    def execute(self):
        for file in self.files: # type: str
            df: pd.DataFrame = pd.read_csv(
                join(self.const.DIR_MACHINE_CSVS, file),
                sep=',',
                low_memory=False
            )

            data_dict: Dict[str, List[any]] = {
                'BEGIN_DATE': [],
                'END_DATE': [],
                'PREV_STATE': [],
                'NEXT_STATE': []
            }

            missing_days: List[str] = []
            for date in self.dates:     # type: str
                if date not in df[self.const.COL_DATE].unique():
                    missing_days.append(date)

            for day in missing_days:    # type: str
                # check whether day is inside an already documented time range and continue if True
                if data_dict:
                    already_checked_days: List[str] = []
                    for index in range(0, len(data_dict['BEGIN_DATE'])):
                        curr_day: datetime.datetime = string_to_date2(data_dict['BEGIN_DATE'][index])
                        end_day: datetime.datetime = string_to_date2(data_dict['END_DATE'][index])

                        already_checked_days.append(curr_day.strftime('%Y-%m-%d'))
                        while curr_day != end_day:
                            curr_day += datetime.timedelta(days=1)
                            already_checked_days.append(curr_day.strftime('%Y-%m-%d'))
                    if day in already_checked_days:
                        continue

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
                    if prev_day_str in df[self.const.COL_DATE].unique():
                        temp_df: pd.DataFrame = df.loc[df[self.const.COL_DATE] == prev_day_str]
                        data_dict['PREV_STATE'].append(temp_df.tail(1)[self.const.COL_STATUS_CODE].values[0])

                    next_day: datetime.datetime = end_date + datetime.timedelta(days=1)
                    temp_df: pd.DataFrame = df.loc[df[self.const.COL_DATE] == next_day.strftime('%Y-%m-%d')]
                    data_dict['NEXT_STATE'].append(temp_df.head(1)[self.const.COL_STATUS_CODE].values[0])
                print(data_dict)
            with open(
                    join(
                        self.const.DIR_DATA_GAPS,
                        "data_gaps_{}.csv".format(df[self.const.COL_MACHINE_NR].values[0])
                    ),
                    "w+"
            ) as out_file:
                out_file.write(pd.DataFrame(data=data_dict).to_csv())

import datetime
from os import mkdir
from os.path import join, exists

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict, List, Tuple

from config import Constants
from utils import get_files_of_dir, string_to_date


class GraphGenerator:

    const: Constants = Constants()

    def __init__(self, start_date, num_of_days):
        self.files: List[str] = get_files_of_dir(self.const.DIR_MACHINE_CSVS)
        self.num_of_days: int = num_of_days
        self.max_length: int = self.num_of_days * 86400

        date: datetime.datetime = string_to_date(start_date)
        self.dates: List[datetime.datetime] = [
            date + datetime.timedelta(days=x) for x in range(0, num_of_days)
        ]
        self.dates = sorted(self.dates)
        self.dates: List[str] = [date.strftime('%Y-%m-%d') for date in self.dates]

        if not exists(self.const.DIR_PLOTS):
            mkdir(self.const.DIR_PLOTS)

    def get_x_values_of_df(
            self,
            df: pd.DataFrame
    ) -> Tuple[np.array, List[str]]:

        begin_seconds: int = 0
        time_range_tuples: List[Tuple[str, int, int]] = []

        previous_row_had_status_code_2: bool = False
        previous_date: str = ''
        for row in df.itertuples():
            if row.STOERTXT_NR == 2 and not previous_row_had_status_code_2:
                begin_seconds = row.BEGIN_ZEIT
                previous_row_had_status_code_2 = True
                previous_date = row.BEGIN_DAT

            elif row.STOERTXT_NR != 2 and previous_row_had_status_code_2:
                if begin_seconds > row.BEGIN_ZEIT and previous_date == row.BEGIN_DAT:
                    # sorting error
                    print("SortingError: entry {} happened BEFORE the previous".format(row.Index))
                    return
                time_range_tuples.append(
                    (row.BEGIN_DAT, begin_seconds, row.BEGIN_ZEIT)
                )
                previous_row_had_status_code_2 = False

        # a day has 86,400 seconds
        value_dict: Dict[str, np.array] = {}
        for date in self.dates:
            value_dict[date] = np.array([np.nan] * 86400)
        # set all status code 2 periods to their respective value
        for time_tuple in time_range_tuples:
            for x in range(time_tuple[1], time_tuple[2] + 1):
                value_dict[time_tuple[0]][x] = x

        # construct one big result array
        result_list: np.array = np.array([])
        days_without_entries: List[str] = []
        num_of_days: int = 1
        for date, time_array in value_dict.items():
            # if date not in dates
            if date not in df.BEGIN_DAT.unique():
                days_without_entries.append(date)
                result_list = np.append(
                    result_list,
                    [np.nan] * 86400
                )
            else:
                result_list = np.append(
                    result_list,
                    [x * num_of_days if x != np.nan else x for x in time_array]
                )
            num_of_days += 1

        return result_list, days_without_entries

    def construct_missing_entries(
            self,
            missing_days: List[str]
    ) -> np.array:
        missing_entries: np.array = np.array([np.nan] * self.max_length)

        day_indices: List[int] = []
        for day in missing_days:
            day_indices.append(self.dates.index(day))

        for index in day_indices:
            for x in range(86400 * index, 86400 * index + 86400):
                missing_entries[x] = x

        return missing_entries

    def generate_plots(self):

        for file in self.files:
            curr_df: pd.DataFrame = pd.read_csv(
                join(self.const.DIR_MACHINE_CSVS, file),
                sep=',',
                low_memory=False
            )

            x_values_and_missing_days: Tuple[List[int], List[str]] = self.get_x_values_of_df(curr_df)
            x_values: List[int] = x_values_and_missing_days[0]
            missing_days: List[str] = x_values_and_missing_days[1]
            missing_entries: List[int] = self.construct_missing_entries(missing_days)

            y_values: np.array = np.array(
                [0 for x in range(0, self.max_length)]
            )

            plt.plot(
                x_values, y_values, 'b-',
                missing_entries, y_values, 'r-',
                lw=4
            )
            plt.axis([-50, self.max_length + 50, -1, 1])
            plt.xlabel('Zeit in s')

            plt.savefig(
                join(self.const.DIR_PLOTS, file.replace('csv', 'png')),
                bbox_inches='tight',
                format='png'
            )
            plt.pause(0.05)

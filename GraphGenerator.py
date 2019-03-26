import datetime
from os import mkdir
from os.path import join, exists

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict, List, Set, Tuple

from config import Constants
from utils import get_files_of_dir, string_to_date2


class GraphGenerator:

    const: Constants = Constants()

    def __init__(self):
        self.files: List[str] = get_files_of_dir(self.const.DIR_MACHINE_CSVS)
        if not exists(self.const.DIR_PLOTS):
            mkdir(self.const.DIR_PLOTS)

    def get_x_values_of_df(
            self,
            df: pd.DataFrame
    ) -> np.array:

        # sorted set containing all of a df's dates in ascending order
        dates: Set[datetime.datetime] = {
            string_to_date2(date) for date in df[self.const.COLUMN_DATE]
        }
        dates = sorted(dates)

        # a day has 86,400 seconds
        value_dict: Dict[str, np.array] = {}
        for date in dates:
            value_dict[date.strftime('%Y-%m-%d')] = np.array([np.nan] * 86400)

        begin_seconds: int = 0
        time_range_tuples: List[Tuple[str, int, int]] = []

        previous_row_had_status_code_2: bool = False
        for row in df.itertuples():
            if row.STOERTXT_NR == 2 and not previous_row_had_status_code_2:
                begin_seconds = row.BEGIN_ZEIT
                previous_row_had_status_code_2 = True

            elif row.STOERTXT_NR != 2 and previous_row_had_status_code_2:
                if begin_seconds >= row.BEGIN_ZEIT:
                    # sorting error
                    print("SortingError: entry {} happened BEFORE the previous".format(row.Index))
                    return
                time_range_tuples.append(
                    (row.BEGIN_DAT, begin_seconds, row.BEGIN_ZEIT)
                )
                previous_row_had_status_code_2 = False

        # set all status code 2 periods to their respective value
        for time_tuple in time_range_tuples:
            for x in range(time_tuple[1], time_tuple[2] + 1):
                value_dict[time_tuple[0]][x] = x

        # construct one big result array
        result_list: List[int] = []
        num_of_days: int = 1
        for date, time_array in value_dict.items():
            result_list.extend(
                [x * num_of_days if x != np.nan else x for x in time_array]
            )
            num_of_days += 1

        return result_list

    def generate_plots(self):
        for file in self.files:
            curr_df: pd.DataFrame = pd.read_csv(
                join(self.const.DIR_MACHINE_CSVS, file),
                sep=',',
                low_memory=False
            )

            x_values: np.array = self.get_x_values_of_df(curr_df)
            print(len(x_values))

            y_values: np.array = np.array(
                [0 for x in range(0, len(x_values))]
            )

            # plot
            plt.plot(
                x_values,
                y_values,
                '-',
                lw=2
            )

            # set proper values for axes
            # xmin, xmax, ymin, ymax
            plt.axis([-50, len(x_values) + 50, -0.01, 0.01])

            # plt.xlabel('time (s)')
            # plt.ylabel('voltage (mV)')
            # plt.title('A sine wave with a gap of NaNs between 0.4 and 0.6')
            # plt.grid(True)

            plt.savefig(
                join(self.const.DIR_PLOTS, file.replace('csv', 'png')),
                bbox_inches='tight',
                format='png'
            )
            plt.pause(0.05)



if __name__ == "__main__":

    t = np.arange(0.0, 1.0 + 0.01, 0.01)
    s = np.cos(2 * 2 * np.pi * t)
    t[41:60] = np.nan

    plt.plot(t, s, '-', lw=2)



    plt.show()

import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict, List, Set, Tuple

from config import Constants
from utils import get_files_of_dir, string_to_date


class GraphGenerator:

    const: Constants = Constants()

    def __init__(self):
        self.files: List[str] = get_files_of_dir(self.const.DIR_MACHINE_CSVS)

    def get_x_values_of_df(
            self,
            df: pd.DataFrame
    ) -> np.array:

        # sorted set containing all of a df's dates in ascending order
        dates: Set[datetime.datetime] = {
            string_to_date(date) for date in df[self.const.COLUMN_DATE]
        }
        dates = sorted(dates)

        value_dict: Dict[str, np.array] = {}
        for date in dates:
            value_dict[date.strftime('%d/%m/%Y')] = np.array([])

        begin_seconds: int = 0
        time_range_tuples: List[Tuple[int, int]] = []

        previous_row_had_status_code_2: bool = False
        for row in df.itertuples():
            if row.STOERTXT_NR == 2 and not previous_row_had_status_code_2:
                begin_seconds = row.BEGIN_ZEIT
                previous_row_had_status_code_2 = True

            elif row.STOERTXT_NR == 2 and previous_row_had_status_code_2:
                begin_seconds = row.BEGIN_ZEIT

            elif row.STOERTXT_NR != 2 and previous_row_had_status_code_2:
                if begin_seconds >= row.BEGIN_ZEIT:
                    # somehow the current entry happened BEFORE the previous? huh?
                    print("whoopsie! entry {} happened BEFORE the previous".format(row.Index))
                    return
                time_range_tuples.append((begin_seconds, row.BEGIN_ZEIT))
            # if neither status_code == 2 nor previous one, ignore entry



if __name__ == "__main__":

    t = np.arange(0.0, 1.0 + 0.01, 0.01)
    s = np.cos(2 * 2 * np.pi * t)
    t[41:60] = np.nan

    # y = list of as many zeroes as x values exist

    plt.subplot(2, 1, 1)
    plt.plot(t, s, '-', lw=2)

    # set proper values for axes
    # xmin, xmax, ymin, ymax
    # plt.axis([0, 10, 0, 20])

    #plt.xlabel('time (s)')
    #plt.ylabel('voltage (mV)')
    #plt.title('A sine wave with a gap of NaNs between 0.4 and 0.6')
    #plt.grid(True)

    plt.subplot(2, 1, 2)
    t[0] = np.nan
    t[-1] = np.nan
    plt.plot(t, s, '-', lw=2)
    plt.title('Also with NaN in first and last point')

    plt.xlabel('time (s)')
    plt.ylabel('more nans')
    plt.grid(True)

    plt.show()

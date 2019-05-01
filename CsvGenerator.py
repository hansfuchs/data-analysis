import datetime
import multiprocessing as mp
from os import mkdir
from os.path import exists, join
import pandas as pd
from typing import Dict, List, Set, Tuple

from Config import Config
import utils


class CsvGenerator:

    def __init__(
            self,
            rows_to_skip: int,
            rows_to_read: int = -1
    ):
        self.rows_to_skip = rows_to_skip
        self.rows_to_read = rows_to_read

        self.conf: Config = Config()

        self.__prepare_environment()
        self.base_files: List[str] = utils.get_files_of_dir(self.conf.DIR_BASE_FILES)

    def __prepare_environment(self):
        if not exists(self.conf.DIR_PREPARED_CSVS):
            mkdir(self.conf.DIR_PREPARED_CSVS)

        if not exists(self.conf.DIR_MACHINE_SERIES_CSVS):
            mkdir(self.conf.DIR_MACHINE_SERIES_CSVS)

        if not exists(self.conf.DIR_MACHINE_CSVS):
            mkdir(self.conf.DIR_MACHINE_CSVS)

    def generate_csv_from_columns(self, file: str):
        print("generating csv from {} ...".format(file))

        curr_df: pd.DataFrame = pd.DataFrame()
        # means rows_to_read wasn't defined
        if self.rows_to_read == -1:
            curr_df = pd.read_csv(
                join(self.conf.DIR_BASE_FILES, file),
                sep='|',
                low_memory=False,
                skiprows=self.rows_to_skip
            )
        else:
            curr_df = pd.read_csv(
                join(self.conf.DIR_BASE_FILES, file),
                sep='|',
                low_memory=False,
                skiprows=self.rows_to_skip,
                nrows=self.rows_to_read
            )

        data_frame = curr_df[[col for col in self.conf.COL_LIST]]
        data_frame = self.reset_index(data_frame)

        generated_filename = '{}_cols_{}.csv'.format(
            join(self.conf.DIR_PREPARED_CSVS, file.split(".")[0]),
            '-'.join(col for col in self.conf.COL_LIST)
        )

        print("\tdone!")
        return generated_filename, data_frame

    def prepare_csvs(self):
        pool = mp.Pool(self.conf.CPU_COUNT)
        for file in self.base_files:
            result = pool.apply_async(
                func=self.generate_csv_from_columns,
                args=(file,)
            )
            with open(result.get()[0], "w+") as output:
                output.write(result.get()[1].to_csv())
        pool.close()
        pool.join()

    def generate_machine_series_csvs(
            self,
            start_date: str,
            num_of_days: int
    ):
        date: datetime.datetime = utils.string_to_date(start_date)
        date_str_list: List[str] = [
            utils.date_to_csv_friendly_str(date + datetime.timedelta(days=x)) for x in range(0, num_of_days)
        ]

        prepared_files: List[str] = utils.get_files_of_dir(self.conf.DIR_PREPARED_CSVS)

        # initialise dict with empty lists for each machine_nr
        machine_dict: Dict[str, List[pd.DataFrame]] = {}
        for machine_nr in self.conf.UNIQUE_MACHINES:  # type: str
            machine_dict[machine_nr] = []

        for file in prepared_files:  # type: str
            print("collecting entries from {} ...".format(file))

            curr_df: pd.DataFrame = pd.read_csv(
                join(self.conf.DIR_PREPARED_CSVS, file),
                sep=',',
                low_memory=False,
            )

            # return early if current csv doesn't contain any date in date_str_list
            curr_df_dates: Set[str] = set(curr_df[self.conf.COL_DATE].values)
            if True not in [date_str in curr_df_dates for date_str in date_str_list]:
                print("{} doesn't contain entries inside date range. skipping.".format(file))
                continue

            unique_machines_in_curr_df: Set[str] = set(curr_df[self.conf.COL_MACHINE_NR].values)
            for machine_nr in self.conf.UNIQUE_MACHINES:  # type: str
                if machine_nr in unique_machines_in_curr_df:
                    machine_df: pd.DataFrame = curr_df.loc[
                        (curr_df[self.conf.COL_MACHINE_NR].str.startswith(machine_nr))

                        & (curr_df[self.conf.COL_DATE].isin(date_str_list))
                    ]

                    if not machine_df.empty:
                        machine_df = self.clean_df(machine_df)
                        machine_df = self.reset_index(machine_df)
                        machine_dict[machine_nr].append(machine_df)

            print("\tdone!")

        for machine_nr in machine_dict:  # type: str
            if machine_dict[machine_nr]:
                filename: str = join(
                    self.conf.DIR_MACHINE_SERIES_CSVS,
                    "{}_{}_until_{}.csv".format(
                        machine_nr,
                        date_str_list[0].replace("/", "-"),
                        date_str_list[-1].replace("/", "-")
                    )
                )
                with open(filename, "w+") as output:
                    df: pd.DataFrame = pd.concat(machine_dict[machine_nr])
                    df = self.reset_index(df)
                    output.write(df.to_csv())

    def generate_machine_csvs(self):
        """ 1) extract all unique machine_nrs from a machine series csv
            2) extract only entries with a status code in ALLOWED_STATUS_CODES and the entry immediately after
            3) sort entries by date and time in ascending order
        """
        machine_series_files: List[str] = utils.get_files_of_dir(self.conf.DIR_MACHINE_SERIES_CSVS)

        # 1)
        for file in machine_series_files:
            curr_df: pd.DataFrame = pd.read_csv(
                join(self.conf.DIR_MACHINE_SERIES_CSVS, file),
                sep=',',
                low_memory=False
            )
            print("collecting entries from {} ...".format(file))

            machine_nr_set: Set[str] = set(curr_df[self.conf.COL_MACHINE_NR])
            for machine_nr in machine_nr_set:
                machine_df: pd.DataFrame = curr_df.loc[
                    curr_df[self.conf.COL_MACHINE_NR] == machine_nr
                ]
                machine_df = self.clean_df(machine_df)

                # 2)
                indices_to_delete: List[int] = []
                prev_row_had_allowed_status: bool = False
                for row in machine_df.itertuples():
                    if row.STOERTXT_NR in self.conf.ALLOWED_STATUS_CODES:
                        prev_row_had_allowed_status = True
                    elif row.STOERTXT_NR not in self.conf.ALLOWED_STATUS_CODES and prev_row_had_allowed_status:
                        prev_row_had_allowed_status = False
                    elif row.STOERTXT_NR not in self.conf.ALLOWED_STATUS_CODES and not prev_row_had_allowed_status:
                        indices_to_delete.append(row.Index)

                machine_df = machine_df.drop(indices_to_delete)

                # 3)
                machine_df[self.conf.COL_DATE] = pd.to_datetime(machine_df.BEGIN_DAT)
                machine_df = machine_df.sort_values(
                    by=[self.conf.COL_DATE, self.conf.COL_TIME]
                )
                machine_df = machine_df.drop_duplicates(self.conf.COL_TIME)
                machine_df = self.reset_index(machine_df)

                filename = join(
                    self.conf.DIR_MACHINE_CSVS,
                    "{}_{}".format(
                        machine_nr,
                        "_".join(file.split("_")[1:])
                    )
                )
                with open(filename, "w+") as output:
                    output.write(machine_df.to_csv())
            print('\tdone!')

    def clean_df(self, df: pd.DataFrame) -> pd.DataFrame:
        # remove column "unnamed"
        return df[[col for col in self.conf.COL_LIST]]

    def reset_index(self, df: pd.DataFrame) -> pd.DataFrame:
        df.index = [x for x in range(0, len(df.index))]
        return df

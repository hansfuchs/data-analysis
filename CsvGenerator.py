import datetime
from os import mkdir
from os.path import exists, join
import pandas as pd
from typing import Dict, List, Set

from config import Constants
import utils


class CsvGenerator:

    def __init__(self):
        self.const: Constants = Constants()
        self.base_files: List[str] = utils.get_files_of_dir(self.const.DIR_BASE_FILES)

        self.__prepare_environment()

    def __prepare_environment(self):
        if not exists(self.const.DIR_PREPARED_CSVS):
            mkdir(self.const.DIR_PREPARED_CSVS)

        if not exists(self.const.DIR_MACHINE_SERIES_CSVS):
            mkdir(self.const.DIR_MACHINE_SERIES_CSVS)

        if not exists(self.const.DIR_MACHINE_CSVS):
            mkdir(self.const.DIR_MACHINE_CSVS)

    def generate_csvs_of_machine_entries(
            self,
            machine_list: List[str],
            start_date: str,
            num_of_days: int
    ):
        """ requires generate_csv_from_columns to be executed beforehand
            since otherwise there would be no generated files
        """
        date: datetime.datetime = utils.string_to_date(start_date)
        date_str_list: List[str] = [
            utils.date_to_csv_friendly_str(date + datetime.timedelta(days=x)) for x in range(0, num_of_days)
        ]

        generated_files: List[str] = utils.get_files_of_dir(self.const.DIR_PREPARED_CSVS)

        # initialise dict with empty lists for each machine_nr
        machine_dict: Dict[str, List[pd.DataFrame]] = {}
        for machine_nr in machine_list:  # type: str
            machine_dict[machine_nr] = []

        for file in generated_files:  # type: str
            print("collecting entries from {} ...".format(file))

            curr_df: pd.DataFrame = pd.read_csv(
                join(self.const.DIR_PREPARED_CSVS, file),
                sep=',',
                low_memory=False,
            )

            # return early if current csv doesn't contain any date in date_str_list
            curr_df_dates: Set[str] = set(curr_df[self.const.COLUMN_DATE].values)
            if True not in [date_str in curr_df_dates for date_str in date_str_list]:
                print("{} doesn't contain entries inside date range. skipping.".format(file))
                continue

            for machine_nr in machine_list:  # type: str
                index_counter: int = 0
                if machine_dict[machine_nr]:
                    # set index_counter to last given index value + 1
                    index_counter = len(machine_dict[machine_nr][-1].index)

                machine_df: pd.DataFrame = curr_df.loc[
                    (curr_df[self.const.COLUMN_MACHINE_NR].str.startswith(machine_nr))
                    & (curr_df[self.const.COLUMN_DATE].isin(date_str_list))
                ]

                if not machine_df.empty:
                    # remove "unnamed" column
                    machine_df = self.clean_df(machine_df)
                    # set index continuing the previous df's index
                    machine_df.index = list(
                        range(index_counter, index_counter + len(machine_df.index))
                    )
                    machine_dict[machine_nr].append(machine_df)

            print("\tdone!")

        self.create_csvs_from_machine_dict(machine_dict, date_str_list)
        return

    def create_csvs_from_machine_dict(
            self,
            machine_dict: Dict[str, List[pd.DataFrame]],
            date_string_list: List[str]
    ):
        for machine_nr in machine_dict:  # type: str
            filename: str = join(
                self.const.DIR_MACHINE_SERIES_CSVS,
                "{}_{}_until_{}.csv".format(
                    machine_nr,
                    date_string_list[0].replace("/", "."),
                    date_string_list[-1].replace("/", ".")
                )
            )
            with open(filename, "w+") as output:
                output.write(pd.concat(machine_dict[machine_nr]).to_csv())

    def generate_csv_from_columns(
            self,
            rows_to_skip: int,
            rows_to_read: int = -1
    ):
        base_files = utils.get_files_of_dir(self.const.DIR_BASE_FILES)

        for file in base_files:
            print("generating csv from {} ...".format(file))

            curr_df: pd.DataFrame = pd.DataFrame()
            # means rows_to_read wasn't defined
            if rows_to_read == -1:
                curr_df = pd.read_csv(
                    join(self.const.DIR_BASE_FILES, file),
                    sep='|',
                    low_memory=False,
                    skiprows=rows_to_skip
                )
            else:
                curr_df = pd.read_csv(
                    join(self.const.DIR_BASE_FILES, file),
                    sep='|',
                    low_memory=False,
                    skiprows=rows_to_skip,
                    nrows=rows_to_read
                )

            data_frame = curr_df[[col for col in self.const.COLUMN_LIST]]
            '''
            for col in data_frame.columns:
                if "$COLUMNS$" in col:
                    data_frame.rename(columns={col: col.split("$COLUMNS$")[-1]}, inplace=True)
                    self.columns[self.columns.index(col)] = col.split("$COLUMNS$")[-1]
            '''

            generated_filename = '{}_cols_{}.csv'.format(
                join(self.const.DIR_PREPARED_CSVS, file.split(".")[0]),
                '-'.join(col for col in self.const.COLUMN_LIST)
            )
            with open(generated_filename, "w+") as output:
                output.write(data_frame.to_csv())

            print("\tdone!")

    def generate_csvs_from_unique_machines(self):
        """ 1) extract all unique machine_nrs from a machine series csv
            2) extract only entries with status code 2 and the following entry
        """
        machine_series_files: List[str] = utils.get_files_of_dir(self.const.DIR_MACHINE_SERIES_CSVS)
        for file in machine_series_files:
            curr_df: pd.DataFrame = pd.read_csv(
                join(self.const.DIR_MACHINE_SERIES_CSVS, file),
                sep=',',
                low_memory=False
            )

            machine_nr_set: Set[str] = set(curr_df[self.const.COLUMN_MACHINE_NR])
            for machine_nr in machine_nr_set:
                machine_df: pd.DataFrame = curr_df.loc[
                    (curr_df[self.const.COLUMN_MACHINE_NR] == machine_nr)
                ]
                machine_df = self.clean_df(machine_df)
                machine_df.index = list(
                    range(0, len(machine_df.index))
                )

                # remove all entries which are not preceded by an entry with status code 2
                indices: List[int] = []
                previous_row_had_status_code_2: bool = False
                for row in machine_df.itertuples():
                    if row.STOERTXT_NR == 2:
                        previous_row_had_status_code_2 = True
                    elif row.STOERTXT_NR != 2 and previous_row_had_status_code_2:
                        previous_row_had_status_code_2 = False
                    elif row.STOERTXT_NR != 2 and not previous_row_had_status_code_2:
                        indices.append(row.Index)
                for index in indices:
                    machine_df = machine_df.drop(index)

                filename = join(
                    self.const.DIR_MACHINE_CSVS,
                    "{}_{}".format(
                        machine_nr,
                        "_".join(file.split("_")[1:])
                    )
                )
                with open(filename, "w+") as output:
                    output.write(machine_df.to_csv())

    def clean_df(
            self,
            df: pd.DataFrame
    ) -> pd.DataFrame:
        # remove column "unnamed"
        return df[[col for col in self.const.COLUMN_LIST]]

from os import mkdir
from os.path import exists, join
import pandas as pd
from typing import List

import config
import utils


class CsvGenerator:

    def __init__(self):
        self.const = config.Constants()
        self.base_files = utils.get_files_of_dir(self.const.DIR_BASE_FILES)

        self.__prepare_environment()

    def __prepare_environment(self):
        if not exists(self.const.DIR_PREPARED_CSVS):
            mkdir(self.const.DIR_PREPARED_CSVS)

        if not exists(self.const.DIR_MACHINE_CSVS):
            mkdir(self.const.DIR_MACHINE_CSVS)

    """
    requires generate_csv_from_columns to be executed beforehand
    since otherwise there would be no generated files
    """
    def generate_csv_for_machine(
            self,
            machine_list: List[str],
            start_date: str,
            num_of_days: int
    ):
        date = utils.string_to_date(start_date)
        generated_files = utils.get_files_of_dir(self.const.DIR_PREPARED_CSVS)

        """ for each file create df for each machine_nr
            might be better than vice versa
        """
        for machine_nr in machine_list:
            df_list = []
            index_counter = 0

            for file in generated_files:
                curr_df = pd.read_csv(
                    join(self.const.DIR_PREPARED_CSVS, file),
                    sep=',',
                    low_memory=False,
                )

                machine_df = curr_df.loc[curr_df[self.const.COLUMN_NAME_OF_MACHINE_NR] == machine_nr]

                if not machine_df.empty:
                    # remove "unnamed" column
                    machine_df = machine_df[[col for col in self.const.COLUMN_LIST]]
                    machine_df.index = [i for i in range(index_counter, index_counter + len(machine_df.index))]

                    df_list.append(machine_df)
                    """ index_counter is set to its last value + the length of
                        the current machine dataframe to avoid duplicate indices
                    """
                    index_counter = len(machine_df.index)

            filename = join(
                self.const.DIR_MACHINE_CSVS,
                "{}_{}_days_{}.csv".format(
                    machine_nr,
                    utils.date_to_string(date),
                    num_of_days
                )
            )
            with open(filename, "w+") as output:
                output.write(pd.concat(df_list).to_csv())

    def generate_csv_from_columns(self, rows_to_skip: int, rows_to_read: int):
        base_files = utils.get_files_of_dir(self.const.DIR_BASE_FILES)

        for file in base_files:
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

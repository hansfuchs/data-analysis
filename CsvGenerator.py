import pandas as pd
from os import mkdir
from os.path import isdir, join

import config


class CsvGenerator:

    def __init__(self, start_date, num_of_days,):
        self.start_date = start_date
        self.num_of_days = num_of_days

        self.const = config.Constants()

        self.__prepare_environment()

    def __prepare_environment(self):
        if not isdir(self.const.DIR_GENERATED_FILES):
            mkdir(self.const.DIR_GENERATED_FILES)

    def generate_csv_for_machine(self, machine_nr):
        for file in self.const.FILE_LIST:
            curr_file = pd.read_csv(
                join(self.const.PATH_ROOT, file),
                sep='|',
                low_memory=False,
                # skiprows=
                # nrows=
            )

    def generate_csv_from_columns(self, rows_to_skip, rows_to_read):
        for file in self.const.FILE_LIST:
            curr_file = pd.read_csv(
                join(self.const.PATH_ROOT, file),
                sep='|',
                low_memory=False,
                skiprows=rows_to_skip,
                nrows=rows_to_read
            )

            data_frame = curr_file[[col for col in self.const.COLUMN_LIST]]

            '''
            for col in data_frame.columns:
                if "$COLUMNS$" in col:
                    data_frame.rename(columns={col: col.split("$COLUMNS$")[-1]}, inplace=True)
                    self.columns[self.columns.index(col)] = col.split("$COLUMNS$")[-1]
            '''

            generated_filename = '{}_cols_{}.csv'.format(
                join(self.const.DIR_GENERATED_FILES, file),
                '-'.join(col for col in self.const.COLUMN_LIST)
            )
            with open(generated_filename, "w+") as output:
                output.write(pd.DataFrame.to_csv(data_frame))

import pandas as pd

import config


class CsvGenerator:
    constants = config.Constants()
    root_directory = constants.DIR_TO_LOOK_IN
    files = constants.FILE_LIST
    columns = constants.COLUMN_LIST

    def __init__(
            self,
            start_date,
            num_of_days,
    ):
        self.start_date = start_date
        self.num_of_days = num_of_days

    def generate_csv_for_machine(self, machine_nr):
        for file in self.files:
            curr_file = pd.read_csv(
                self.root_directory + file,
                sep='|',
                low_memory=False,
                #skiprows=
                #nrows=
            )

    def generate_csv_from_columns(self, rows_to_skip, rows_to_read):
        for file in self.files:
            curr_file = pd.read_csv(
                self.root_directory + file,
                sep='|',
                low_memory=False,
                skiprows=rows_to_skip,
                nrows=rows_to_read
            )

            data_frame = curr_file[[col for col in self.columns]]

            for col in data_frame.columns:
                if "$COLUMNS$" in col:
                    data_frame.rename(columns={col: col.split("$COLUMNS$")[-1]}, inplace=True)
                    self.columns[self.columns.index(col)] = col.split("$COLUMNS$")[-1]

            generated_filename = file + "_cols_" + '-'.join(col for col in self.columns) + ".csv"
            with open(generated_filename, "w+") as output:
                output.write(pd.DataFrame.to_csv(data_frame))

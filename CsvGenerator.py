import pandas as pd


class CsvGenerator:
    def __init__(
            self,
            start_date,
            num_of_days,
            root_directory,
            files,
            suffix,
            columns
    ):
        self.start_date = start_date
        self.num_of_days = num_of_days
        self.root_directory = root_directory
        self.files = files
        self.suffix = suffix
        self.columns = columns

    def generate_csv_for_machine(self, machine_nr):
        for file in self.files:
            curr_file = pd.read_csv(
                self.root_directory + file + self.suffix,
                sep='|',
                low_memory=False,
                #skiprows=
                #nrows=
            )

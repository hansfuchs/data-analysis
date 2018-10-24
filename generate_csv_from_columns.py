import pandas as pd

import config.csv_generator_enums as e


def generate_csv_from_columns(file_list, column_list):
    for file in file_list:
        curr_file = pd.read_csv(e.FileDetails.DIR_TO_LOOK_IN.value +
                                file +
                                e.FileDetails.SUFFIX.value,
                                sep='|',
                                low_memory=False,
                                skiprows=e.Constants.NUMBER_OF_LINES_TO_SKIP.value,
                                nrows=e.Constants.NUMBER_OF_LINES_TO_READ.value)

        data_frame = curr_file[[col for col in column_list]]

        for col in data_frame.columns:
            if "$COLUMNS$" in col:
                data_frame.rename(columns={col: col.split("$COLUMNS$")[-1]}, inplace=True)
                column_list[column_list.index(col)] = col.split("$COLUMNS$")[-1]

        generated_filename = file + "_cols_" + '-'.join(col for col in column_list) + ".csv"
        with open(generated_filename, "w+") as output:
            output.write(pd.DataFrame.to_csv(data_frame))


if __name__ == "__main__":
    generate_csv_from_columns(e.Constants.FILE_LIST.value,
                              e.Constants.COLUMN_LIST.value)

import pandas as pd
import config.enums as e


def generate_csv_from_columns(file_list, column_list):
    data_frame_list = []

    for file in file_list:
        for column in column_list:
            curr_file = pd.read_csv(e.FileDetails.DIR_TO_LOOK_IN.value +
                                    file + e.FileDetails.SUFFIX.value,
                                    sep='|',
                                    low_memory=False)
            df = pd.DataFrame(curr_file[column])

            if "$COLUMNS$" in column:
                sub_arr = column.split("$COLUMNS$")
                column_list[column_list.index(column)] = sub_arr[-1]
                df[sub_arr[-1]] = df.pop(column)

            data_frame_list.append(df)
        data_frame = pd.concat(data_frame_list)

        generated_filename = file + "_cols_" + '-'.join(col for col in column_list) + ".csv"
        with open(generated_filename, "w+") as output:
            output.write(pd.DataFrame.to_csv(data_frame))


if __name__ == "__main__":
    generate_csv_from_columns(e.CsvGeneratorParameters.FILE_LIST.value,
                              e.CsvGeneratorParameters.COLUMN_LIST.value)

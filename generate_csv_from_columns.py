import os
import pandas as pd


def get_root_path():
    path_list = os.path.realpath(__file__).split("\\")
    return '\\'.join(path_list[:len(path_list)-1], )


def generate_csv_from_columns(root_path, file_list, column_list):
    dir_to_look_in = "\\Kunde1\\"

    file_list = (file + ".unl" for file in file_list)
    data_frame_list = []

    for file in file_list:
        for column in column_list:
            curr_file = pd.read_csv(root_path + dir_to_look_in + file,
                                    sep='|',
                                    low_memory=False)
            data_frame_list.append(pd.DataFrame(curr_file[column]))

        data_frame = pd.concat(data_frame_list)
        with open(file + "_cols_" + '_'.join(col for col in column_list) + ".csv", "w+") as output:
            output.write(pd.DataFrame.to_csv(data_frame))


if __name__ == "__main__":
    fileList = [
        "a_ereignis_01"
    ]
    columnList = [
        "$COLUMNS$MASCH_NR"
    ]
    ROOT_PATH = get_root_path()
    print(ROOT_PATH)
    generate_csv_from_columns(ROOT_PATH, fileList, columnList)

from CsvGenerator import CsvGenerator
import config.csv_generator_enums as e


def main():

    csv_generator = CsvGenerator(
        "07/24/2013",
        "",
        e.Constants.DIR_TO_LOOK_IN,
        e.Constants.FILE_LIST,
        e.Constants.COLUMN_LIST
    )


if __name__ == "__main__":
    main()

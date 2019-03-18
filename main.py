from CsvGenerator import CsvGenerator


def main():
    csv_generator = CsvGenerator(
        "07/24/2013",
        "30"
    )
    csv_generator.generate_csv_from_columns(0, 20)


if __name__ == "__main__":
    main()

from CsvGenerator import CsvGenerator


def main():

    csv_generator: CsvGenerator = CsvGenerator()
    """
    csv_generator.generate_csv_from_columns(0)

    csv_generator.generate_csvs_of_machine_entries(
        [
            # group all entries in one csv that start with these patterns
            "BFO4A"
        ],
        # dd/mm/yyyy
        "07/24/2013",
        1
    )
    """
    csv_generator.generate_csvs_from_unique_machines()


if __name__ == "__main__":
    main()

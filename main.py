from CsvGenerator import CsvGenerator


def main():
    csv_generator: CsvGenerator = CsvGenerator()
    csv_generator.generate_csv_from_columns(0, 20)
    csv_generator.generate_csv_for_machine(
        [
            "BFO4AP02"
        ],
        # dd/mm/yyyy
        "07/24/2013",
        1
    )


if __name__ == "__main__":
    main()

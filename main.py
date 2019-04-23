from CsvGenerator import CsvGenerator
from GraphGenerator import GraphGenerator


def main():

    csv_generator: CsvGenerator = CsvGenerator()

    #csv_generator.generate_csv_from_columns(0)
    
    #csv_generator.generate_csvs_of_unique_machines(
    #     [
             # group all entries in one csv that start with these patterns
    #         "BFO4A",
             #"WFL1",
             #"BFL"
    #     ],
         # mm/dd/yyyy
    #     "07/24/2013",
    #     14
    #)

    csv_generator.generate_csvs_from_unique_machines()

    #graph_generator: GraphGenerator = GraphGenerator("07/24/2013", 14)
    #graph_generator.generate_plots()


if __name__ == "__main__":
    main()

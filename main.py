from CsvGenerator import CsvGenerator
from DataGapClassifier import DataGapClassifier
from GraphGenerator import GraphGenerator


if __name__ == "__main__":
    csv_generator: CsvGenerator = CsvGenerator(
        rows_to_skip=0
    )

    #csv_generator.prepare_csvs()
    #csv_generator.generate_machine_series_csvs(
    # mm/dd/yyyy
    #    "07/24/2013",
    #    696
    #)
    csv_generator.generate_machine_csvs()

    # graph_generator: GraphGenerator = GraphGenerator("07/24/2013", 14)
    # graph_generator.generate_plots()

    # data_gap_classifier: DataGapClassifier = DataGapClassifier("2013-07-24", 14)
    # data_gap_classifier.extract_data_gaps()
    # data_gap_classifier.group_gaps()

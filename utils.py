import datetime
from os import listdir
from os.path import isfile, join
from typing import List


def get_files_of_dir(directory: str) -> List[str]:
    return [file for file in listdir(directory) if isfile(join(directory, file))]


def string_to_date(date_string: str) -> datetime.datetime:
    date_list: List[int] = [int(date) for date in date_string.split("/")]
    return datetime.datetime(
        date_list[2],
        date_list[0],
        date_list[1]
    )


def date_to_csv_friendly_str(date: datetime.datetime) -> str:
    return "{}/{}/{}".format(
        date.month if len(str(date.month)) == 2 else "0" + str(date.month),
        date.day if len(str(date.day)) == 2 else "0" + str(date.day),
        date.year
    )


def get_datetime_from_date_and_seconds(
        seconds: str,
        date: datetime.datetime
) -> datetime.datetime:
    return date + datetime.timedelta(seconds=float(seconds))

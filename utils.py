import datetime
from os import listdir
from os.path import isfile, join
from typing import List


def get_files_of_dir(directory: str) -> List[str]:
    return [file for file in listdir(directory) if isfile(join(directory, file))]


# mm/dd/YYYY
def string_to_date(date_str: str) -> datetime.datetime:
    date_list: List[int] = [int(date) for date in date_str.split("/")]
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


# YYYY-mm-dd
def string_to_date2(date_str: str) -> datetime.datetime:
    date_list: List[int] = [int(date) for date in date_str.split("-")]
    return datetime.datetime(
        date_list[0],
        date_list[1],
        date_list[2]
    )


def get_amount_of_days(datestr_1: str, datestr_2: str) -> int:
    date1: datetime.datetime = string_to_date2(datestr_1)
    date2: datetime.datetime = string_to_date2(datestr_2)
    delta: datetime.timedelta = date2 - date1
    return delta.days + 1

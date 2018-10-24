from enum import Enum
import FsModule


class SystemDetails(Enum):
    ROOT_PATH = FsModule.get_root_path()


class FileDetails(Enum):
    DIR_TO_LOOK_IN = SystemDetails.ROOT_PATH.value + "\\Kunde1\\"
    SUFFIX = ".unl"


class CsvGeneratorParameters(Enum):
    FILE_LIST = [
        "a_ereignis_01"
    ]
    COLUMN_LIST = [
        "$COLUMNS$MASCH_NR"
    ]

from enum import Enum
import FsModule


class SystemDetails(Enum):
    ROOT_PATH = FsModule.get_root_path()


class FileDetails(Enum):
    DIR_TO_LOOK_IN = SystemDetails.ROOT_PATH.value + "\\Kunde1\\"
    SUFFIX = ".unl"


class Constants(Enum):
    FILE_LIST = [
        "a_ereignis_01"
    ]
    COLUMN_LIST = [
        "$COLUMNS$MASCH_NR",
        "BEGIN_ZEIT",
        "ENDE_ZEIT"
    ]
    NUMBER_OF_LINES_TO_READ = 100
    NUMBER_OF_LINES_TO_SKIP = 0

from enum import Enum

ARG_TYPES = {
    "--time",
    "--company",
    "--role",
    "--location",
    "--level",
    "--source",
    "--count"
}

class Valid_Args(Enum):
    SIZE = 7
    TIME = 0
    COMPANY = 1
    ROLE = 2
    LOCATION = 3
    LEVEL = 4
    SOURCE = 5
    COUNT = 6
    

class Columns(Enum):
    ARGS_SIZE = 12
    APPLICATION_LINK = 0
    ID = 1
    COMPANY_NAME = 2
    ROLE = 3
    LOCATION = 4
    DATE_POSTED = 5
    TIME_POSTED = 6
    DATE_SCRAPED = 7
    TIME_SCRAPED = 8
    SCRAPED_SOURCES = 9
    LEVEL = 10
    COUNT = 11
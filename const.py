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
    ARGS_SIZE = 14
    JOB_COUNTER = 0
    GRP_ID = 1
    APPLICATION_LINK = 2
    ID = 3
    COMPANY_NAME = 4
    ROLE = 5
    LOCATION = 6
    DATE_POSTED = 7
    TIME_POSTED = 8
    DATE_SCRAPED = 9
    TIME_SCRAPED = 10
    SCRAPED_SOURCE = 11
    LEVEL = 12
    COUNT = 13
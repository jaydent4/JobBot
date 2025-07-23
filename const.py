from enum import Enum

ARG_TYPES = {
    "--time",
    "--company",
    "--role",
    "--city",
    "--state",
    "--level",
    "--source",
    "--count"
}

class Valid_Args(Enum):
    SIZE = 8
    TIME = 0
    COMPANY = 1
    ROLE = 2
    CITY = 3
    STATE = 4
    LEVEL = 5
    SOURCE = 6
    COUNT = 7
    

class Columns(Enum):
    ARGS_SIZE = 14
    JOB_COUNTER = 0
    GRP_ID = 1
    APPLICATION_LINK = 2
    ID = 3
    COMPANY_NAME = 4
    ROLE = 5
    CITY = 6
    STATE = 7
    DATE_POSTED = 8
    TIME_POSTED = 9
    DATE_SCRAPED = 10
    TIME_SCRAPED = 11
    SCRAPED_SOURCE = 12
    LEVEL = 13
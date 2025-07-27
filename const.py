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

US_STATE_TO_ABBRE: dict[str, str] = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "Virgin Islands, U.S.": "VI",
}
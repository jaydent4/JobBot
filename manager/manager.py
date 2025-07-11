import sqlite3
from config import Config
import importlib
from logging_config import setup_logging
import pandas as pd

# dB contains repeats (marked in the repost col)

class Manager:
    def __init__(self, sources):

         # sets up logger
        self.logger = setup_logging("Manager", "INFO", "INFO", "manager.log")
        print(self.logger)

        self.sources = sources
        #print(self.sources)
        
        # puts scrapers in dict[str, Obj] ex: github: GitHubScraper (object)
        self.scrapers = {}

        # loads all the scrapers
        self.load_scrapers()

        
        # we can have another dB act as cachce? but how do we ensure temporal and spacial locality?

        # following: https://docs.python.org/3/library/sqlite3.html
        try:
            with sqlite3.connect('job.db') as self.conn:
                self.cur = self.conn.cursor()

                # creates a dB if there isn't one yet; opens existing dB if there is
                self.cur.execute(
                    """ CREATE TABLE IF NOT EXISTS jobPostings(
                        id INTEGER PRIMARY KEY, 
                        company_name TEXT NOT NULL, 
                        role TEXT NOT NULL, 
                        location TEXT NOT NULL, 
                        application_link TEXT NOT NULL, 
                        date_posted DATE NOT NULL,
                        time_posted TIME NOT NULL, 
                        date_scraped DATE NOT NULL,
                        time_scraped TIME NOT NULL, 
                        scrape_source TEXT NOT NULL
                        );"""
                )

                # commit the changes
                self.conn.commit()

                print("Table created successfully.")
        except sqlite3.OperationalError as e:
            print("Failed to", e)

        # TRYING TO LOAD FAKE DATA AND INSERT INTO DB, IT WORKS BTW
        data = pd.read_csv("./manager/fake_data.csv")
        print(data)
        data = data.values.tolist()

        try:
            self.cur.executemany("INSERT INTO jobPostings VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
            self.conn.commit()
            print('hi') # when its in db it won't insert it again (hi does not get printed)
        except Exception as e:
            self.logger.error(f"Something errored while inserting scrapped job postings into the main database: {e}")
 
        for row in self.cur.execute("SELECT * FROM jobPostings ORDER BY id"):
            print(row)
        
        # need to calculate today's date and the input argument ex: --time 5 day and then input that somehow as a query to sql

        print("------")
        # checking queries, but how to make sure we dont' ahve 10! query cases?
        # queryResult = self.cur.execute("""SELECT * FROM jobPostings 
        #                                WHERE company_name = 'amazon' (side note: this also works: WHERE company_name in ('amazon'))
        #                                AND role = 'ML'
        #                                AND date_posted > '2025-06-01'
        #                                AND time_posted >= '01:04' (side note can also do: time_posted > '01:04:00.000')
        #                                """)
        queryResult = self.cur.execute("""SELECT * FROM jobPostings 
                                       WHERE company_name in ('amazon')
                                       AND role = 'ML'
                                       """)
        for row in queryResult:
            print(row)

    """
    Attempt to load all scrapers from configurations
    """
    def load_scrapers(self):
        for name in self.sources:
            module_name = "scrapers." + name.lower()
            try:
                self.logger.info(f'Attempting to load module: {module_name}')
                module = importlib.import_module(module_name)
                scraper = getattr(module, name.upper() + "Scraper")
                self.scrapers[name] = scraper()
            except Exception as e:
                self.logger.error(f'Something occurred while attempting to load {module_name}: {e}')
    
    """
    Args:
        name: name of the scraper/site
    Returns:
        list[tuple]: each tuple is a separate job posting, each tuple must contain 10 elements in the order of the columns in the database
    """
    def scrape(self, name) -> list[tuple] | None:
        if not self.scrapers[name]:
            return None
        return self.scrapers[name].scrape()

    """
    Args:
        None

    Returns:
        dict: containing unique job postings from all scrapers
    """
    def run_scrapers(self):
        result = {}
        for name in self.scrapers.keys():
            result[name] = self.scrape(name)
        # need to parse for uniqueness after result is populated
        return result


    """
    Calls scrapers then checks if dB updated
    Args:
        None

    Returns:
        (tuple[bool, dict]): bool is true if dB updated, bool is false if dB did not update, dict is the dictionary of new postings
    """
    def update(self):
        newPostings = self.run_scrapers()
        # cache would be updated somewhere in this method
        if len(newPostings) > 0:
            self.updateDB()
            return (True, newPostings)
        else:
            return (False, None)
        
    
    # if we have a getter, we need a setter right lmao
    # needs to check against existing postings, if it already exists, make sure to mark the repost col
    """
    Inserts scrapped job postings into the main database
    Args:

    Returns:
        None
    """
    def update_DB(self, jobpostings: list[tuple]) -> None:
        try:
            self.cur.executemany("INSERT INTO jobPostings VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", jobpostings)
            self.conn.commit()
        except Exception as e:
            self.logger.error(f"Something errored while inserting scrapped job postings into the main database: {e}")

    
    """
    Doc strings
    """
    def get_data(self, args: tuple):
        # parse args
        self.parse_args(args)
        # if there is a time argument like -time 5 days, need to calculate what that new date is from today's date

        # how do we not have like 10! cases...
        # https://codedamn.com/news/sql/how-to-write-multiple-where-conditions-in-sql
        # https://docs.python.org/3/library/sqlite3.html


        # reference job method in main.py
        # lists all postings of type x (ML, SWE, etc) *need to check validity
        # lists all postings at location x (Ca, NY, etc) *need to chekc validity, like if i pass in moon
        # lists all postings from company x (amazon, meta, etc) *need to chekc validity
        # lists all postings in the last 10 days (default of --time 10 d)

        # personally i think its more useful for user to query the bot rather than have bot maintain info about which user wants what-
        pass

    
    """
    Parses arguments into a dictionary
    Args:
        args: tuple of arguments passed from discord bot
    
    Returns:
        dict: arguments parsed into a dictionary, None if arguments are invalid
    """
    # temporary arg parser, will fix later
    def parse_args(self, args: tuple) -> dict:
        parsed_args = {}
        arg_type = None
        for arg in args:
            if not arg_type and arg.startswith("--"):
                arg_type = arg[2:]
            elif arg_type and not arg.startswith("--"):
                parsed_args[arg_type] = arg
                arg_type = None
            else:
                self.logger.error(f' {arg_type}: {arg} is an invalid argument')
                return None
        return parsed_args

        


        
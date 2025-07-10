import sqlite3
from config import Config
import importlib
from logging_config import setup_logging

# dB contains repeats (marked in the repost col)

class Manager:
    def __init__(self):
        config = Config()

         # sets up logger
        self.logger = setup_logging("Manager", "INFO", "INFO", "manager.log")
        print(self.logger)

        self.sources = list(config.sources.keys())
        #print(self.sources)
        
        # puts scrapers in dict[str, str] ex: github: GitHubScraper (object)
        self.scrapers = {}

        # loads all the scrapers
        self.load_scrapers()

        # not sure if rate is needed here
        self.updateRate = config.rate
        
        # we can have another dB act as cachce? but how do we ensure temporal and spacial locality?

        # following: https://docs.python.org/3/library/sqlite3.html
        try:
            with sqlite3.connect('job.db') as conn:
                cur = conn.cursor()

                # creates a dB if there isn't one yet; opens existing dB if there is
                cur.execute(
                    """ CREATE TABLE IF NOT EXISTS jobPostings(
                        id INTEGER PRIMARY KEY, 
                        company_name TEXT NOT NULL, 
                        role TEXT NOT NULL, 
                        location TEXT NOT NULL, 
                        application_link TEXT NOT NULL, 
                        time_posted DATE NOT NULL, 
                        time_scraped DATE NOT NULL, 
                        scrape_source TEXT NOT NULL,
                        repost INT NOT NULL
                        );"""
                )

                # commit the changes
                conn.commit()

                print("Table created successfully.")
        except sqlite3.OperationalError as e:
            print("Failed to", e)

        pass

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
        scrape results (TBD)
    """
    def scrape(self, name):
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
        self.updateDB()
        if len(newPostings) > 0:
            return (True, newPostings)
        else:
            return (False, None)
        
    
    # if we have a getter, we need a setter right lmao
    # needs to check against existing postings, if it already exists, make sure to mark the repost col
    def updateDB(self):
        pass

    
    """
    Doc strings
    """
    def getData(self, args: tuple):
        # gonna parse input data here or in another method in manager

        # reference job method in main.py
        # lists all postings of type x (ML, SWE, etc) *need to check validity
        # lists all postings at location x (Ca, NY, etc) *need to chekc validity, like if i pass in moon
        # lists all postings from company x (amazon, meta, etc) *need to chekc validity
        # lists all postings in the last 10 days (default of --time 10 d)

        # personally i think its more useful for user to query the bot rather than have bot maintain info about which user wants what-
        pass

        
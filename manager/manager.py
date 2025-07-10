from config import Config
import importlib
from logging_config import setup_logging

# reference the drawing
# dB contains repeats (marked in the repost col)
"""
dB cols:

job id
compnay name
role
loc
link
time posted
time scraped
source scrapped
repost
"""

class Manager:
    def __init__(self, config: Config):
        self.sources = list(config.sources.keys())
        self.scrapers = {}
        self.rate = config.rate
        self.logger = setup_logging("Manager", "INFO", "INFO", "manager.log")
    
    """
    Attempt to load all scrapers from configurations
    """
    def load_scrapers(self):
        for name in self.sources:
            module_name = "scrapers." + name.lower() + "_scraper"
            try:
                self.logger.info(f'Attempting to load module: {module_name}')
                module = importlib.import_module(module_name)
                scraper = getattr(module, name.captialize + "Scraper")
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

        
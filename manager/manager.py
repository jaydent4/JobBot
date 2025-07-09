# imports all the scrapers

# reference the drawing

class Manager:
    def __init__(self):
        # puts scrapers in list
        pass
    

    """
    Doc strings
    """
    def call_scraper(self):
        pass


    """
    updates the database by calling scrapers
    Args:


    Returns:
        T/F based on if the dB got updated
    """
    def update(self):
        pass
    

    """
    Doc strings

    This should deal with cache
    """
    def getUpdatedInfo(self):
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

    # if we have a getter, we need a setter right lmao
    def setData(self):
        pass
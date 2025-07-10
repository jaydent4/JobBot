from scrapers.github import GitHubScraper
import sqlite3

# reference the drawing
# dB contains repeats (marked in the repost col)

class Manager:
    def __init__(self):
        # makes all the scraper objects here
        github = GitHubScraper()
        # puts scrapers in list
        # creates a dB if there isn't one yet; opens existing dB if there is
        # we can have another dB act as cachce? but how do we ensure temporal and spacial locality?

        # following: https://docs.python.org/3/library/sqlite3.html
        try:
            with sqlite3.connect('job.db') as conn:
                cur = conn.cursor()

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

    Args:
        None

    Returns:
        dict: containing unique job postings from all scrapers
    """
    def run_scrapers(self):
        pass


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

    
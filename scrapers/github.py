from base import ScraperBase
import requests
from bs4 import BeautifulSoup

class GITHUBScraper(ScraperBase):
    def __init__(self):
        pass

    """
    Scapes job information off of GitHub README Repos of job postings
    Args:
        args: cls
    
    Returns:
        not sure yet
    """
    @classmethod
    def scrape(cls):
        url = "https://github.com/SimplifyJobs/Summer2026-Internships"
        result = requests.get(url).text
        doc = BeautifulSoup(result, "html.parser")

        job_tables = doc.find_all("markdown-accessiblity-table")
        print(job_tables)



if __name__ == "__main__":
    GITHUBScraper.scrape()

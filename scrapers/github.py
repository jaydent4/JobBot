from scrapers.base import ScraperBase
import requests
from bs4 import BeautifulSoup

class GITHUBScraper(ScraperBase):
    def __init__(self):
        pass

    @classmethod
    def scrape(cls):
        url = "https://github.com/SimplifyJobs/Summer2026-Internships"
        result = requests.get(url).text
        doc = BeautifulSoup(result, "html.parser")

        job_tables = doc.find('markdown-accessibility-table')  

        print(job_tables)


if __name__ == "__main__":
    GITHUBScraper.scrape()

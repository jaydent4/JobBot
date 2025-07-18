from base import ScraperBase
import requests
from bs4 import BeautifulSoup
from datetime import datetime 
# from const import Columns

class ycombinatorScraper(ScraperBase):
    def __init__(self, url):
        self.url = url
    
    def scrape(self) -> list[tuple] | None:
        page = requests.get(self.url).content
        soup = BeautifulSoup(page, "lxml")
        res = soup.find_all("table")
        links = soup.find_all("a")
        meta_data = soup.find_all("meta")
        for row in meta_data:
            print(row)
        # for row in links:
        #     print(row)
        # for row in res:
        #     print("\n")
        #     print(row)
        return None
    

if __name__ == "__main__":
    scraper = ycombinatorScraper(url="https://news.ycombinator.com/jobs")
    scraper.scrape()
from base import ScraperBase
import requests
from bs4 import BeautifulSoup
from datetime import datetime 

class ycombinatorScraper(ScraperBase):
    def __init__(self, url):
        self.url = url
    
    def scrape(self) -> list[tuple] | None:
        page = requests.get(self.url).content
        doc = BeautifulSoup(page, "lxml")
        #print(doc.prettify())
        res = doc.find_all("table")
        print(res)
        return None
    

if __name__ == "__main__":
    scraper = ycombinatorScraper(url="https://news.ycombinator.com/jobs")
    scraper.scrape()
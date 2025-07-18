from base import ScraperBase
import requests
from bs4 import BeautifulSoup
from datetime import datetime 
from const import Columns

class ycombinatorScraper(ScraperBase):
    def __init__(self, url):
        self.scraped_source = "ycombinator"
        self.url = url
    
    def scrape(self) -> list[tuple] | None:
        self.datetime = datetime.now()
        self.date_scraped = self.datetime.date()
        self.time_scraped = self.datetime.time()

        page = requests.get(self.url).content
        soup = BeautifulSoup(page, "lxml")

        links = soup.find_all("a")

        job_grpings: list[tuple] = []
        left = 0
        for i in range(len(links)):
            content = links[i].contents
            text = links[i].text
            if "(YC )" in content:
                curr_job_posting = ["NONE"] * Columns.ARGS_SIZE.value
                curr_job_posting[Columns.COMPANY_NAME.value] = 
                
            print(content, links[i], links[i]["href"])
        # for row in tables:
        #     tbody = row.find_all("td")

        #     print("\n")
        #     print(tbody)
        return None
    

if __name__ == "__main__":
    scraper = ycombinatorScraper(url="https://news.ycombinator.com/jobs")
    scraper.scrape()
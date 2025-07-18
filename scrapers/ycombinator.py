from base import ScraperBase
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from const import Columns

class ycombinatorScraper(ScraperBase):
    def __init__(self, url):
        self.scraped_source = "ycombinator"
        self.ycombo_joburl_base = "https://news.ycombinator.com/" #"https://news.ycombinator.com/item?id=44573320"
        default = "NONE"
        self.url = url
    
    def scrape(self) -> list[tuple] | None:
        self.datetime = datetime.now()
        self.date_scraped = self.datetime.date()
        self.time_scraped = self.datetime.time()

        print(self.date_scraped)

        page = requests.get(self.url).content
        soup = BeautifulSoup(page, "lxml")

        links = soup.find_all("a")

        job_grpings: list[tuple] = []
        left = 0
        for i in range(len(links)):
            whole_tag = links[i]
            text = links[i].text
            if " (YC" in text:
                print(text[:text.index(" (YC")])
                curr_job_posting = ["NONE"] * Columns.ARGS_SIZE.value

                if "item" in links[i]["href"]:
                    curr_job_posting[Columns.APPLICATION_LINK.value] = self.ycombo_joburl_base + links[i]["href"]
                else:
                    curr_job_posting[Columns.APPLICATION_LINK.value] = links[i]["href"]

                curr_job_posting[Columns.ID.value] = None
                curr_job_posting[Columns.ROLE.value] = "NONE"
                curr_job_posting[Columns.COMPANY_NAME.value] = text[:text.index(" (YC")]
                curr_job_posting[Columns.SCRAPED_SOURCE.value] = self.scraped_source
                curr_job_posting[Columns.DATE_SCRAPED.value] = str(self.date_scraped)
                curr_job_posting[Columns.TIME_SCRAPED.value] = str(self.time_scraped)

            print(text, whole_tag, links[i]["href"])
        # for row in tables:
        #     tbody = row.find_all("td")

        #     print("\n")
        #     print(tbody)
        return None
    

if __name__ == "__main__":
    scraper = ycombinatorScraper(url="https://news.ycombinator.com/jobs")
    scraper.scrape()
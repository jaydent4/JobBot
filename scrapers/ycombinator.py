from base import ScraperBase
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from config import Config
from enum import Enum

class Columns(Enum):
    ARGS_SIZE = 12
    APPLICATION_LINK = 0
    ID = 1
    COMPANY_NAME = 2
    ROLE = 3
    LOCATION = 4
    DATE_POSTED = 5
    TIME_POSTED = 6
    DATE_SCRAPED = 7
    TIME_SCRAPED = 8
    SCRAPED_SOURCE = 9
    LEVEL = 10
    COUNT = 11

class ycombinatorScraper(ScraperBase):
    def __init__(self):
        self.scraped_source = "ycombinator"
        self.ycombo_joburl_base = "https://news.ycombinator.com/" #"https://news.ycombinator.com/item?id=44573320"
        default = "NONE"
        self.url = "https://news.ycombinator.com/jobs"
    
    def scrape(self, job_counter, grp_counter) -> list[tuple] | None:
        self.datetime = datetime.now()
        self.date_scraped = self.datetime.date()
        self.time_scraped = self.datetime.time()

        print(self.date_scraped)

        page = requests.get(self.url).content
        page_soup = BeautifulSoup(page, "lxml")

        links = page_soup.find_all("a")

        job_grpings: list[tuple] = []
        left = 0
        for i in range(20):
            whole_tag = links[i]
            text = links[i].text
            print(text, whole_tag)
            if " (YC" in text:
                print(text[:text.index(" (YC")])
                curr_job_posting:list = ["NONE"] * (Columns.ARGS_SIZE.value - 1)

                job_link = ""
                if "item" in links[i]["href"]:
                   job_link = self.ycombo_joburl_base + links[i]["href"]
                else:
                    job_link = links[i]["href"]

                # second scrap
                print("----")
                job_page = requests.get(job_link).content
                job_soup = BeautifulSoup(job_page, "lxml")
                tds = job_soup.find_all("table")
                print(tds)
                desc = job_soup.find_all("script", {"type": "application/ld+json"})
                print(desc)
                # for j in range(len(job_links)):
                #     print(job_links[j])
                print("----")
                
                curr_job_posting[Columns.APPLICATION_LINK.value] = job_link
                curr_job_posting[Columns.ID.value] = None
                curr_job_posting[Columns.ROLE.value] = "NONE"
                curr_job_posting[Columns.COMPANY_NAME.value] = text[:text.index(" (YC")]
                curr_job_posting[Columns.ROLE.value] = "NONE"
                curr_job_posting[Columns.LOCATION.value] = "NONE"
                curr_job_posting[Columns.DATE_POSTED.value] = "NONE"
                curr_job_posting[Columns.TIME_POSTED.value] = "NONE"
                curr_job_posting[Columns.DATE_SCRAPED.value] = str(self.date_scraped)
                curr_job_posting[Columns.TIME_SCRAPED.value] = str(self.time_scraped)
                curr_job_posting[Columns.SCRAPED_SOURCE.value] = self.scraped_source
                curr_job_posting[Columns.LEVEL.value] = "NONE"
            
            
                print(curr_job_posting)
        # for row in tables:
        #     tbody = row.find_all("td")

        #     print("\n")
        #     print(tbody)
        return None
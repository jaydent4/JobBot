from base import ScraperBase
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from const import Columns, US_STATE_TO_ABBRE
from enum import Enum
from clean_url import clean_url
import json

# class Columns(Enum):
#     ARGS_SIZE = 14
#     APPLICATION_LINK = 0
#     ID = 1
#     COMPANY_NAME = 2
#     ROLE = 3
#     LOCATION = 4
#     DATE_POSTED = 5
#     TIME_POSTED = 6
#     DATE_SCRAPED = 7
#     TIME_SCRAPED = 8
#     SCRAPED_SOURCE = 9
#     LEVEL = 10
#     COUNT = 11

class ycombinatorScraper(ScraperBase):
    def __init__(self, url):
        self.job_id = 0
        self.grp_id = 0
        self.scraped_source = "ycombinator"
        self.ycombo_joburl_base = "https://news.ycombinator.com/" #"https://news.ycombinator.com/item?id=44573320"
        self.url = url
        self.type_one_set = set(("title", "datePosted", "employmentType", "jobLocation"))
    
    def scrape(self) -> list[tuple] | None:
        # use update_config_value
        # use trim_url
        # use merkle somehow
        self.datetime = datetime.now()
        self.date_scraped = self.datetime.date()
        self.time_scraped = self.datetime.time()

        print(self.date_scraped)

        page = requests.get("https://news.ycombinator.com/item?id=44603739").content
        page_soup = BeautifulSoup(page, "lxml")
        print(page_soup.prettify())
        links = page_soup.find_all("a")

        job_grpings: list[tuple] = []
        left = 0
        # for i in range(20): # parses 1 whole page, 30 posts
        #     #1 type1: https://www.ycombinator.com/companies/spice-data/jobs/RJz1peY-product-associate-new-grad
        #     # type2: https://jobs.ashbyhq.com/extend, https://www.optery.com/careers/
        #     #2 type3: https://news.ycombinator.com/item?id=44603739
        #     # type4: https://www.ycombinator.com/companies/martin/jobs/
        #     # type5: https://jobs.ashbyhq.com/meticulous/3197ae3d-bb26-4750-9ed7-b830f640515e
        #     # https://www.ycombinator.com/companies/martin/jobs/
        #     text = links[i].text
        #     if " (YC" in text:
        #         # print(text[:text.index(" (YC")])
        #         curr_job_posting:list = ["NONE"] * (Columns.ARGS_SIZE.value)
        #         locs_on_post = []
        #         role, date_posted, time_posted, level = "NONE", "NONE", "NONE", "NONE"

        #         app_link = ""
        #         if "item" in links[i]["href"]:
        #             app_link = self.ycombo_joburl_base + links[i]["href"]
        #         else:
        #             app_link = links[i]["href"]

        #         # second scrap
        #         print("----")
        #         job_page = requests.get(app_link).content
        #         job_soup = BeautifulSoup(job_page, "lxml")
        #         # print(job_soup.prettify())

        #         # tds = job_soup.find_all("table")
        #         # print(tds)
                
        #         # t1
        #         desc = str(job_soup.find_all("script", {"type": "application/ld+json"}))
        #         if '{' in desc:
        #             print(desc)
        #             # print(desc[desc.index("{"): -10])
        #             print(json.loads(desc[desc.index("{"): -10]))
        #             job_info = dict(json.loads(desc[desc.index("{"): -10]))
        #             print(job_info.keys())
        #             if self.type_one_set.issubset(set(job_info.keys())):
        #                 role = job_info["title"]
        #                 date_posted = job_info["datePosted"][:10]
        #                 time_posted = job_info["datePosted"][12:-1]
        #                 level = job_info["employmentType"]
        #                 locs = job_info["jobLocation"]

        #                 for l in locs:
        #                     address = l["address"]
        #                     city = address["addressLocality"]
        #                     state = US_STATE_TO_ABBRE[address["addressRegion"]]
        #                     locs_on_post.append((city, state))

        #             # for j in range(len(job_links)):
        #             #     print(job_links[j])
        #         print("----")
                
        #         for city, state in locs_on_post:
        #             curr_job_posting[Columns.JOB_COUNTER.value] = self.job_id
        #             self.job_id += 1

        #             curr_job_posting[Columns.GRP_ID.value] = self.grp_id
        #             curr_job_posting[Columns.APPLICATION_LINK.value] = clean_url(app_link)
        #             curr_job_posting[Columns.ID.value] = None
        #             curr_job_posting[Columns.COMPANY_NAME.value] = text[:text.index(" (YC")]
        #             curr_job_posting[Columns.ROLE.value] = role
        #             curr_job_posting[Columns.CITY.value] = city
        #             curr_job_posting[Columns.STATE.value] = state
        #             curr_job_posting[Columns.DATE_POSTED.value] = date_posted
        #             curr_job_posting[Columns.TIME_POSTED.value] = time_posted
        #             curr_job_posting[Columns.DATE_SCRAPED.value] = str(self.date_scraped)
        #             curr_job_posting[Columns.TIME_SCRAPED.value] = str(self.time_scraped)
        #             curr_job_posting[Columns.SCRAPED_SOURCE.value] = self.scraped_source
        #             curr_job_posting[Columns.LEVEL.value] = level

        #             job_grpings.append(tuple(curr_job_posting))

        #         self.grp_id += 1
            

        #         print(curr_job_posting)

        print(job_grpings)
        # for row in tables:
        #     tbody = row.find_all("td")

        #     print("\n")
        #     print(tbody)
        return None
    

if __name__ == "__main__":
    scraper = ycombinatorScraper(url="https://news.ycombinator.com/jobs")
    scraper.scrape()
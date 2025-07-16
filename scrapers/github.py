from .base import ScraperBase
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class githubScraper(ScraperBase):
    def __init__(self, url):
        pass

    """
    Scapes job information off of GitHub README Repos of job postings
    Args:
        args: cls
    
    Returns:
        List of tuples
    """
    def scrape(self, url) -> list[tuple]:
        url = "https://github.com/SimplifyJobs/Summer2026-Internships"
        result = requests.get(url).text
        doc = BeautifulSoup(result, "lxml")

        job_tables = doc.find_all("table")
        job_data = []

        date_scraped = datetime.now().strftime("%d %b %Y")
        time_scraped = datetime.now().strftime("%H:%M")

        for table in job_tables[1:]:
            tbody = table.find("tbody")
            rows = tbody.find_all("tr")

            prev_company = None
            for row in rows:
                cols = row.find_all("td")
                #insert date check here so don't have to have all the extra memory/time running to add to list and just dont add if so
    
                current_job_data = [col.get_text(strip=True) for i, col in enumerate(cols) if i != 3]

                # checks if post date is within 0-2 days
                if self.filter_date(current_job_data):
                    if current_job_data[0] != "↳":
                        prev_company = current_job_data[0]
                    else:
                        current_job_data[0] = prev_company

                    job_id = None
                    company = current_job_data[0]
                    role = current_job_data[1]
                    location = current_job_data[2]
                    link = "NONE"
                    date_posted = "NONE"
                    time_posted = "NONE"
                    level = "intern"

                    job_info = (
                        job_id,
                        company,
                        role,
                        location,
                        link,
                        date_posted,
                        time_posted,
                        date_scraped,
                        time_scraped,
                        "GitHub",
                        level
                    )
                    job_data.append(job_info)

        # for i in job_data:
        #     print(i)
        #     print()
        # print(job_data)
        return job_data


    def filter_date(self, job_data) -> bool:
        date_ranges = ["0d", "1d", "2d"]
        if job_data[3] not in date_ranges:
            return False
        return True


# if __name__ == "__main__":
    # githubScraper.scrape()

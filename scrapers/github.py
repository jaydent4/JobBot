from base import ScraperBase
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class GITHUBScraper(ScraperBase):
    def __init__(self):
        pass

    """
    Scapes job information off of GitHub README Repos of job postings
    Args:
        args: cls
    
    Returns:
        List of tuples
    """
    @classmethod
    def scrape(cls) -> list[tuple]:
        url = "https://github.com/SimplifyJobs/Summer2026-Internships"
        result = requests.get(url).text
        doc = BeautifulSoup(result, "lxml")

        job_tables = doc.find_all("table")
        job_data = []

        for table in job_tables[1:]:
            tbody = table.find("tbody")
            rows = tbody.find_all("tr")

            prev_company = None
            for row in rows:
                current_job_data = []
                cols = row.find_all("td")

                current_job_data = [col.get_text(strip=True) for i, col in enumerate(cols) if i != 3]

                # checks if post date is within 0-2 days
                if cls.filter_date(current_job_data):
                    if current_job_data[0] != "↳":
                        prev_company = current_job_data[0]
                    else:
                        current_job_data[0] = prev_company

                    job_info = tuple(current_job_data)
                    job_data.append(job_info)

        for i in job_data:
            print(i)
            print()
        # print(job_data)

    @staticmethod
    def filter_date(job_data) -> bool:
        date_ranges = ["0d", "1d", "2d"]
        if job_data[3] not in date_ranges:
            return False
        return True


if __name__ == "__main__":
    GITHUBScraper.scrape()

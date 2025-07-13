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

        job_tables = doc.find_all("table")
        job_data = []

        for table in job_tables[1:]:
            tbody = table.find("tbody")
            # print(tbody)
            # print()

            rows = tbody.find_all("tr")
            for row in rows:
                cols = row.find_all("td")
                job_info = tuple(col.get_text(strip=True) for col in cols)

                job_data.append(job_info)

        for job in job_data[:60]:
            print(job)



if __name__ == "__main__":
    GITHUBScraper.scrape()

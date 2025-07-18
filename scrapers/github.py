from base import ScraperBase
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
# from const import Columns

class githubScraper(ScraperBase):
    def __init__(self, url):
        self.url = url

    """
    Scapes job information off of GitHub README Repos of job postings
    Args:
        args: cls
    
    Returns:
        List of tuples
    """
    def scrape(self) -> list[tuple]:
        # url = "https://github.com/SimplifyJobs/Summer2026-Internships"
        result = requests.get(self.url).text
        doc = BeautifulSoup(result, "lxml")

        job_tables = doc.find_all("table")
        job_data = []

        date_scraped = datetime.now().strftime("%Y %b %d")
        time_scraped = datetime.now().strftime("%H:%M")

        for table in job_tables[1:]:
            tbody = table.find("tbody")
            rows = tbody.find_all("tr")

            prev_company = None
            for row in rows:
                cols = row.find_all("td")

                # checks if post date is within 0-2 days
                if cols[4].get_text(strip=True) not in ["0d", "1d", "2d", "3d"]:
                    continue

                current_job_data = [col.get_text(strip=True).encode("ascii", "ignore").decode("ascii") for i, col in enumerate(cols) if i != 3]

                # replaces filler subcategories
                if current_job_data[0]:
                    prev_company = current_job_data[0]
                else:
                    current_job_data[0] = prev_company
                print(current_job_data)

                posted_date = datetime.now() - timedelta(days=int(current_job_data[3][0]))
                link_data = cols[3].find("a")

                job_id = None
                company = current_job_data[0]
                role = current_job_data[1]
                location = current_job_data[2]
                link = link_data.get("href") if link_data else "None"
                date_posted = posted_date.strftime("%Y %b %d")
                time_posted = posted_date.strftime("%H:%M")
                level = "intern"

                job_info = (
                    link,
                    job_id,
                    company,
                    role,
                    location,
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
        # print(job_data)
        return job_data


if __name__ == "__main__":
    scraper = githubScraper("https://github.com/SimplifyJobs/Summer2026-Internships")
    scraper.scrape()

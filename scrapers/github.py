from base import ScraperBase
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
from const import US_STATE_TO_ABBRE


class githubScraper(ScraperBase):
    def __init__(self):
        self.url = "https://github.com/SimplifyJobs/Summer2026-Internships"


    """
    Scapes job information off of GitHub README Repos of job postings
    Args:
        args: cls
    
    Returns:
        List of tuples
    """
    def scrape(self, job_counter, grp_id) -> list[tuple]:
        result = requests.get(self.url).text
        doc = BeautifulSoup(result, "lxml")

        job_tables = doc.find_all("table")
        job_data = []

        date_scraped = datetime.now().strftime("%Y-%m-%d")
        time_scraped = datetime.now().strftime("%H:%M")

        for table in job_tables[1:]:
            tbody = table.find("tbody")
            rows = tbody.find_all("tr")

            prev_company = None

            for row in rows:
                cols = row.find_all("td")
                if len(cols) == 1:
                    break
                
                current_job_data = [col.get_text(strip=True).encode("ascii", "ignore").decode("ascii") for i, col in enumerate(cols) if i != 3]
                
                # stop grabbing roles when the date is passed
                if current_job_data[3] not in {"0d", "1d", "2d", "3d"}:
                    break
                posted_date = datetime.now() - timedelta(days=int(current_job_data[3][0]))
                if current_job_data[0]:
                    prev_company = current_job_data[0]
                else:
                    current_job_data[0] = prev_company

                link_data = cols[3].find("a")

                job_id = None
                company = current_job_data[0]
                role = current_job_data[1]
                location = self.parse_location(current_job_data[2])
                link = link_data.get("href") if link_data else "None"
                date_posted = posted_date.strftime("%Y-%m-%d")
                time_posted = posted_date.strftime("%H:%M")
                level = "Intern"

                for loc in location:
                    city, state = loc[0], loc[1]

                    job_info = (
                        job_counter,
                        grp_id,
                        link,
                        job_id,
                        company,
                        role,
                        city,
                        state,
                        date_posted,
                        time_posted,
                        date_scraped,
                        time_scraped,
                        "GitHub",
                        level
                    )
                    job_data.append(job_info)
                    job_counter += 1
                grp_id += 1

        return job_data


    def parse_location(self, locations):
            locations = locations.strip()
            result = []

            pattern = r'([A-Za-z .]+?),?\s*([A-Z]{2})'
            matches = re.findall(pattern, locations)

            for city, state in matches:
                city = city.strip()
                result.append((city, state))

            if not result:
                state = US_STATE_TO_ABBRE.get(locations)
                if state:
                    result.append((locations, state))
                else:
                    result.append((locations, None))
            return result

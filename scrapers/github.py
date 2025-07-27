from base import ScraperBase
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
# from const import US_STATE_TO_ABBRE

US_STATE_TO_ABBRE: dict[str, str] = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "Virgin Islands, U.S.": "VI",
}




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

        job_counter = 0
        grp_id = 0

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
                # print(current_job_data)

                posted_date = datetime.now() - timedelta(days=int(current_job_data[3][0]))
                link_data = cols[3].find("a")

                job_id = None
                company = current_job_data[0]
                role = current_job_data[1]
                location = self.parse_location(current_job_data[2])
                link = link_data.get("href") if link_data else "None"
                date_posted = posted_date.strftime("%Y %b %d")
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

        for i in job_data:
            print(i)
        # print(job_data)
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


if __name__ == "__main__":
    scraper = githubScraper("https://github.com/SimplifyJobs/Summer2026-Internships")
    scraper.scrape()

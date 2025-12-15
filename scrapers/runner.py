import os
import sys
from scrapers.registry import SCRAPER_REGISTRY

def main():
    if len(sys.argv) < 2:
        raise RuntimeError("Usage: runner.py <scraper-name>")

    scraper_name = sys.argv[1]

    if scraper_name not in SCRAPER_REGISTRY:
        raise ValueError(f"Unknown scraper: {scraper_name}")

    url = os.environ["SCRAPER_URL"]
    job_counter = int(os.environ.get("JOB_COUNTER", "0"))
    grp_id = os.environ.get("GROUP_ID", "default")

    scraper_cls = SCRAPER_REGISTRY[scraper_name]
    scraper = scraper_cls(url)

    results = scraper.scrape(job_counter, grp_id)

    print(f"Scraped {len(results)} jobs")

if __name__ == "__main__":
    main()

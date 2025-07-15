from .base import ScraperBase
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class ycombinatorScraper(ScraperBase):
    def __init__(self):
        pass
    

    @classmethod
    def scrape(self) -> list[tuple] | None:
        return None
    
    

if __name__ == "__main__":
    ycombinatorScraper.scrape()
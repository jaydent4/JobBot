from abc import ABC, abstractmethod

class ScraperBase(ABC):
    def __init__(self, url):
        pass
    """
    Scrapers are responsible for updating global job_counter and grp_id values 
    as they get the jobpostings

    also responsible for link trimming
    """
    @classmethod
    @abstractmethod
    def scrape(self) -> list[tuple]:
        pass
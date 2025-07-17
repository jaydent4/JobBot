from abc import ABC, abstractmethod

class ScraperBase(ABC):
    def __init__(self, url):
        pass
    
    @classmethod
    @abstractmethod
    def scrape(self) -> list[tuple]:
        pass
from abc import ABC, abstractmethod

class ScraperBase(ABC):
    def __init__(self):
        pass
    
    @classmethod
    @abstractmethod
    def scrape(self):
        pass
from abc import ABC, abstractmethod

class base(ABC):
    @abstractmethod
    def __init__(self):
        pass
    
    @classmethod
    @abstractmethod
    def scrape(self):
        pass
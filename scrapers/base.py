from abc import ABC, abstractmethod, classmethod

class base(ABC):
    @abstractmethod
    def __init__(self):
        pass
    
    @classmethod
    @abstractmethod
    def scrape(self):
        pass
from abc import abstractmethod, classmethod

class base:
    @abstractmethod
    def __init__(self):
        pass
    
    @classmethod
    @abstractmethod
    def scrape(self):
        pass
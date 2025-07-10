import yaml
from logging_config import setup_logging

"""
JobBot Configurations; the YAML will follow the following format:

sources:
    source1: str
    source2: str
channel: int
rate: float

"default_config.yml" serves as an example and the default configuration
"""

class Config:
    def __init__(self, config="defautl_config.yml"):
        with open(config, 'r') as f:
            config_data = yaml.load(f, Loader=yaml.FullLoader)
            self.sources = config_data["sources"]
            self.channel = config_data["channel"]
            self.rate = config_data["rate"]
    
    def display_config(self):
        logger = setup_logging("config_logger", "DEBUG", "DEBUG")
        logger.info(f'PRINTING CONFIG:\n\tsources: {self.sources}')
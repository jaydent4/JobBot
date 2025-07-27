import yaml
from logging_config import setup_logging

"""
JobBot Configurations; the YAML will follow the following format:

sources:
    source1: str
    source2: str
channel: int
rate: float
job_counter: int
grp_id: int

"default_config.yml" serves as an example and the default configuration
"""

class Config:
    def __init__(self, config="default_config.yml"):
        with open(config, 'r') as f:
            config_data = yaml.load(f, Loader=yaml.FullLoader)
            self.sources = config_data["sources"]
            self.channel = config_data["channel"]
            self.rate = config_data["rate"]
            self.job_counter = config_data["job_counter"]
            self.grp_id = config_data["grp_id"]
        
    def display_config(self):
        logger = setup_logging("config_logger", "DEBUG", "DEBUG")
        logger.info(f'PRINTING CONFIG:\n\tsources: {self.sources}\n\tchannel: {self.channel}\n\trate: {self.rate}\n')
    
    def update_config_value(self, key: str, val: int, config="default_config.yml"):
        if key not in set(("job_counter", "grp_id")):
            raise AssertionError("wrong use of update config value buddy")

        with open(config, 'r') as f:
            config_data = yaml.load(f, Loader=yaml.FullLoader)
        
        with open(config, 'w') as f:
            if key == "job_counter":
                self.job_counter += val
            elif key == "grp_id":
                self.grp_id += val
            config_data[key] += val
            yaml.dump(config_data, f, default_flow_style=False)
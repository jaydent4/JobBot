import yaml

class Config:
    def __init__(self, file='./utils/config.yml'):
        with open(file, 'r') as f:
            config_data = yaml.load(f, Loader=yaml.FullLoader)
            self.channel = config_data["channel"]
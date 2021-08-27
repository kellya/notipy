import yaml

""" Create a config object to manage configuration details """


class Config:
    """The config class to hold config details"""

    def __init__(self):
        self.config = None

    def load_config(self, configfile):
        """Load the configuration from specified file"""
        try:
            with open(configfile, "r") as config_file:
                config_entries = yaml.safe_load(config_file)
        except FileNotFoundError as error:
            print(error)
            return False
        else:
            self.config = config_entries

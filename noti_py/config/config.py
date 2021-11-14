""" Create a config object to manage configuration details """
import yaml

class Config:  # pylint: disable=too-few-public-methods
    """Create an object to track config options "too few public methods" be damned :)"""

    def __init__(self):
        self.config = None

    def load_config(self, configfile):
        """Method to read the configfile and return a"""
        try:
            with open(configfile, "r", encoding="UTF-8") as config_file:
                config_entries = yaml.safe_load(config_file)
        except FileNotFoundError as error:
            print(error)
            return False
        else:
            self.config = config_entries
        return True

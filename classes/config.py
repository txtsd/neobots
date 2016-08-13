# ---------------------------------------------------------------------
# ---------------------------- neobots --------------------------------
# ------------------------------txtsd----------------------------------
# ---------------------------------------------------------------------

"""Handles the configuration file"""

from collections import OrderedDict
import json
import os


class Config:

    dir_data = 'data'
    dir_logs = 'logs'
    file_config = 'config.json'
    file_accounts = 'accounts.txt'

    default_config = OrderedDict(
        {
            'username': '',
            'password': '',
            'proxy': '',
            'neoPin': '',
        }
    )

    def __init__(self, account):
        self.config = None
        self.refresh()

    def get(self, key):
        try:
            return self.config[key]
        except KeyError:
            return False

    def set(self, key, value):
        try:
            self.config[key] = value
            return True
        except:
            return False

    def refresh(self):
        if os.path.isfile(Config.file_config):
            with open(Config.file_config, 'r') as file:
                self.config = json.load(file, object_pairs_hook=OrderedDict)
        else:
            self.config = self._create_config()

    def sync(self):
        with open(Config.file_config, 'w') as file:
            json.dump(self.config, file, indent=2)

    def _create_config(self):
        with open(Config.file_config, 'w') as file:
            json.dump(Config.default_config, file, indent=2)
        self.refresh()

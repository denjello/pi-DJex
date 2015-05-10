import json
import os

class DjexConfig:

    data = {
        "rmswindowsize": 2,
        "threshold": 80,
        "gpio_pins": {
            "active": 11,
            "pwm_warn": 12,
            "relay": 22
        }
    }

    last_modified = 0

    def update(self):
        if os.path.isfile('config.json'):
            stats = os.stat('config.json')
            if stats.st_mtime != self.last_modified:
                with open('config.json', 'r') as infile:
                    self.last_modified = stats.st_mtime
                    self.data = json.load(infile)
        else:
            self.dump()

    def dump(self):
        with open('config.json', 'w') as outfile:
            json.dump(self.data, outfile)

    def get(self, key):
        return self.data[key]

    def set(self, key, val):
        self.data[key] = val
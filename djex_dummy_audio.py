import random
import time

class DjexDummyAudio():

    input = {}
    config = {}
    rms = 0

    def configure(self, config):
        self.config = config

    def initaudio(self):
        print("dummy audio init")

    def main(self):
        self.rms = random.randint(0, 100)
        time.sleep(.1)
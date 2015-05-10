import time

class DjexDummyGpio:

    debug = False
    pwm = False
    warn = False
    config = {}

    def setup(self, config):

        self.config = config
        print("dummy gpio initialized")

    def send_warning(self):
        if self.warn:
            return

        self.warn = True

        print("WEE")
        time.sleep(0.2)
        print("OOO")
        time.sleep(0.2)
        print("WEE")
        time.sleep(0.2)
        print("OOO")
        time.sleep(0.2)
        print("WEE")
        time.sleep(0.2)
        print("OOO")
        print("")
        self.warn = False

    def cleanup(self):
        print("dummy gpio cleanup")
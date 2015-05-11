import RPi.GPIO as GPIO
import time

class DjexPiGpio:

    debug = False
    pwm = False
    warn = False
    config = {}

    def setup(self, config):

        self.config = config

        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(self.config["gpio_pins"]["active"], GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #enable pull down resistor

        GPIO.setup(self.config["gpio_pins"]["relay"], GPIO.OUT)
        GPIO.setup(self.config["gpio_pins"]["warn"], GPIO.OUT)

        self.pwm = GPIO.PWM(self.config["gpio_pins"]["warn"], 1000)
        self.pwm.start(50)  # 50 %

    def send_warning(self):
        if self.warn:
            return

        self.warn = True
        GPIO.output(self.config["gpio_pins"]["relay"], GPIO.HIGH)

        self.pwm.ChangeDutyCycle(50)
        time.sleep(0.2)
        self.pwm.ChangeDutyCycle(0)
        time.sleep(0.2)
        self.pwm.ChangeDutyCycle(50)
        time.sleep(0.2)
        self.pwm.ChangeDutyCycle(0)
        time.sleep(0.2)
        self.pwm.ChangeDutyCycle(50)
        time.sleep(0.2)
        self.pwm.ChangeDutyCycle(0)
        self.warn = False

    def cleanup(self):
        GPIO.cleanup
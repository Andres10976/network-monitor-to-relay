import RPi.GPIO as GPIO
import logging

logger = logging.getLogger(__name__)

class Relay:
    def __init__(self, pin: int):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)
        logger.info(f"Relay initialized on pin {self.pin}")

    def activate(self):
        GPIO.output(self.pin, GPIO.HIGH)
        logger.info("Relay activated")

    def deactivate(self):
        GPIO.output(self.pin, GPIO.LOW)
        logger.info("Relay deactivated")

    def __del__(self):
        GPIO.cleanup(self.pin)
        logger.info("GPIO cleaned up")
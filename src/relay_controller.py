import RPi.GPIO as GPIO
import logging

logger = logging.getLogger(__name__)

class RelayController:
    def __init__(self, pin: int):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.active = False

    def activate(self):
        GPIO.output(self.pin, GPIO.HIGH)
        self.active = True
        logger.info(f"Relay on pin {self.pin} activated")

    def deactivate(self):
        GPIO.output(self.pin, GPIO.LOW)
        self.active = False
        logger.info(f"Relay on pin {self.pin} deactivated")

    def is_active(self) -> bool:
        return self.active

    def cleanup(self):
        GPIO.cleanup(self.pin)
        logger.info(f"Cleaned up GPIO pin {self.pin}")
import RPi.GPIO as GPIO
from src.logger import setup_logger

logger = setup_logger(__name__)

class RelayController:
    def __init__(self, pin: int):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    async def activate(self):
        logger.info(f"Activating relay on pin {self.pin}")
        GPIO.output(self.pin, GPIO.HIGH)

    async def deactivate(self):
        logger.info(f"Deactivating relay on pin {self.pin}")
        GPIO.output(self.pin, GPIO.LOW)

    def cleanup(self):
        GPIO.cleanup(self.pin)
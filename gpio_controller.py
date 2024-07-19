import RPi.GPIO as GPIO

class GPIOController:
    def __init__(self, pin, logger):
        self.pin = pin
        self.logger = logger
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def activate(self):
        GPIO.output(self.pin, GPIO.HIGH)
        self.logger.info(f"GPIO pin {self.pin} activated")

    def deactivate(self):
        GPIO.output(self.pin, GPIO.LOW)
        self.logger.info(f"GPIO pin {self.pin} deactivated")

    def cleanup(self):
        GPIO.cleanup()
        self.logger.info("GPIO cleanup completed")
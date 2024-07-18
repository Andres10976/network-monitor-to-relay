import logging

logger = logging.getLogger(__name__)

class MockGPIO:
    OUT = "OUT"
    HIGH = "HIGH"
    LOW = "LOW"
    BCM = "BCM"

    @staticmethod
    def setmode(mode):
        logger.info(f"GPIO mode set to {mode}")

    @staticmethod
    def setup(pin, mode):
        logger.info(f"Pin {pin} set up as {mode}")

    @staticmethod
    def output(pin, state):
        logger.info(f"Pin {pin} set to {state}")

    @staticmethod
    def cleanup():
        logger.info("GPIO cleanup performed")
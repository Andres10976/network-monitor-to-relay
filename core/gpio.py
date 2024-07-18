import logging
import os

logger = logging.getLogger(__name__)

# Check if we're running on a Raspberry Pi
try:
    import RPi.GPIO as GPIO
except ImportError:
    from .mock_gpio import MockGPIO as GPIO
    logger.warning("RPi.GPIO not available. Using mock GPIO.")

def setup_gpio(pins):
    try:
        GPIO.setmode(GPIO.BCM)
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
        logger.info(f"GPIO pins {pins} set up successfully")
    except Exception as e:
        logger.error(f"Error setting up GPIO: {e}")
        raise

def activate_relay(pin):
    try:
        GPIO.output(pin, GPIO.HIGH)
        logger.info(f"Relay on pin {pin} activated")
    except Exception as e:
        logger.error(f"Error activating relay on pin {pin}: {e}")

def deactivate_relay(pin):
    try:
        GPIO.output(pin, GPIO.LOW)
        logger.info(f"Relay on pin {pin} deactivated")
    except Exception as e:
        logger.error(f"Error deactivating relay on pin {pin}: {e}")

def cleanup_gpio():
    GPIO.cleanup()
    logger.info("GPIO cleaned up")
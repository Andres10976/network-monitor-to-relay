import yaml
import logging
import logging.config
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from config.config_validator import validate_config
from core.ping import ping_all
from core.gpio import setup_gpio, activate_relay, deactivate_relay, cleanup_gpio
from utils.ip import get_all_ips

# Setup logging
logging.config.fileConfig('logging.conf')
logger = logging.getLogger()

def load_config():
    with open('config/config.yml', 'r') as config_file:
        config_dict = yaml.safe_load(config_file)
    return validate_config(config_dict)

def main():
    config = load_config()
    all_ips = get_all_ips(config.dict())
    all_pins = list(all_ips.keys())

    setup_gpio(all_pins)
    relay_activated = {pin: False for pin in all_pins}

    logger.info(f"Starting to monitor IPs: {all_ips}")
    logger.info("Press CTRL+C to stop the script")

    # Check if we're using mock GPIO
    if 'RPi' not in globals():
        logger.warning("Running with mock GPIO. Pin activations will be logged but not actually performed.")

    try:
        while True:
            with ThreadPoolExecutor(max_workers=config.max_threads) as executor:
                future_to_pin = {
                    executor.submit(
                        ping_all, 
                        all_ips[pin], 
                        config.ping.dict(), 
                        config.reconnect.dict()
                    ): pin for pin in all_pins
                }

                for future in as_completed(future_to_pin):
                    pin = future_to_pin[future]
                    try:
                        unreachable_ips = future.result()
                        if unreachable_ips and not relay_activated[pin]:
                            activate_relay(pin)
                            relay_activated[pin] = True
                            logger.info(f"Relay on pin {pin} activated. Unreachable IPs: {', '.join(unreachable_ips)}")
                        elif not unreachable_ips and relay_activated[pin]:
                            deactivate_relay(pin)
                            relay_activated[pin] = False
                            logger.info(f"All IPs for pin {pin} reachable. Relay deactivated.")
                    except Exception as e:
                        logger.error(f"Error processing IPs for pin {pin}: {e}")

            if any(relay_activated.values()):
                time.sleep(config.cycle_interval.alert)
            else:
                time.sleep(config.cycle_interval.normal)

    except KeyboardInterrupt:
        logger.info("Script terminated by user")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    finally:
        cleanup_gpio()
        logger.info("Exiting.")

if __name__ == "__main__":
    main()
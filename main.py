import logging
import logging.config
from ip_monitor.config import load_config
from ip_monitor.monitor import IPMonitor

def main():
    # Load logging configuration
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger(__name__)

    try:
        # Load and validate configuration
        config = load_config()

        # Create and start the IP monitor
        monitor = IPMonitor(config)
        monitor.start()

    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()
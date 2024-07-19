import signal
import sys
from ping_monitor import PingMonitor
from config_loader import load_config
from logger import setup_logger

def graceful_shutdown(signum, frame):
    logger.info("Graceful shutdown initiated...")
    monitor.cleanup()
    sys.exit(0)

if __name__ == "__main__":
    config = load_config()
    logger = setup_logger(config['log_file'], config['log_level'])

    signal.signal(signal.SIGINT, graceful_shutdown)
    signal.signal(signal.SIGTERM, graceful_shutdown)

    monitor = PingMonitor(config, logger)
    monitor.run()
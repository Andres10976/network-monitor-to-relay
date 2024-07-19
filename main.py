import asyncio
import signal
from src.config_manager import ConfigManager
from src.ip_monitor import IPMonitor
from src.relay_controller import RelayController
import logging
import logging.config

# Set up logging
logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

async def main():
    # Load configuration
    config = ConfigManager('config.yml')
    
    # Initialize components
    relay_controller = RelayController(config.relay_pin)
    ip_monitor = IPMonitor(config, relay_controller)

    # Set up graceful shutdown
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown(ip_monitor, relay_controller)))

    try:
        # Start monitoring
        await ip_monitor.start_monitoring()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        await shutdown(ip_monitor, relay_controller)

async def shutdown(ip_monitor: IPMonitor, relay_controller: RelayController):
    logger.info("Shutting down...")
    await ip_monitor.stop_monitoring()
    relay_controller.cleanup()
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    await asyncio.gather(*tasks, return_exceptions=True)
    asyncio.get_running_loop().stop()

if __name__ == "__main__":
    asyncio.run(main())
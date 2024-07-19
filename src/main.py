import asyncio
import signal
from src.config_manager import ConfigManager
from src.ip_scanner import IPScanner
from src.relay_controller import RelayController
from src.logger import setup_logger

logger = setup_logger(__name__)

async def main():
    # Load configuration
    config = ConfigManager('config/config.yml')
    
    # Initialize components
    relay_controller = RelayController(config.relay_pin)
    ip_scanner = IPScanner(config, relay_controller)

    # Setup graceful shutdown
    loop = asyncio.get_event_loop()
    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
    for s in signals:
        loop.add_signal_handler(
            s, lambda s=s: asyncio.create_task(shutdown(s, loop, ip_scanner))
        )

    try:
        await ip_scanner.start_monitoring()
    finally:
        await ip_scanner.stop_monitoring()

async def shutdown(signal, loop, ip_scanner):
    logger.info(f"Received exit signal {signal.name}...")
    await ip_scanner.stop_monitoring()
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()

if __name__ == "__main__":
    asyncio.run(main())
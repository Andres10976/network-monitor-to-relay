import asyncio
from ipaddress import ip_address
from src.config_manager import ConfigManager
from src.relay_controller import RelayController
from src.ping_utils import ping_ip
import logging

logger = logging.getLogger(__name__)

class IPMonitor:
    def __init__(self, config: ConfigManager, relay_controller: RelayController):
        self.config = config
        self.relay_controller = relay_controller
        self.running = False

    async def start_monitoring(self):
        self.running = True
        while self.running:
            await self.monitor_ips()
            await asyncio.sleep(self.config.ping_interval)

    async def stop_monitoring(self):
        self.running = False

    async def monitor_ips(self):
        ip_range = self.get_ip_range()
        tasks = [self.check_ip(ip) for ip in ip_range]
        results = await asyncio.gather(*tasks)
        
        if not all(results):
            logger.warning("Some IPs are not responding")
            await self.handle_failed_pings()
        elif self.relay_controller.is_active():
            logger.info("All IPs are responding, deactivating relay")
            self.relay_controller.deactivate()

    def get_ip_range(self):
        start, end = self.config.ip_range
        ip_range = [ip_address(ip) for ip in range(int(ip_address(start)), int(ip_address(end)) + 1)]
        ip_range = [ip for ip in ip_range if str(ip) not in self.config.passlist]
        ip_range.extend([ip_address(ip) for ip in self.config.whitelist])
        return list(set(ip_range))  # Remove duplicates

    async def check_ip(self, ip):
        for _ in range(self.config.retry_count):
            if await ping_ip(str(ip)):
                return True
            await asyncio.sleep(self.config.retry_delay)
        logger.warning(f"IP {ip} is not responding after {self.config.retry_count} attempts")
        return False

    async def handle_failed_pings(self):
        if not self.relay_controller.is_active():
            logger.info("Activating relay due to failed pings")
            self.relay_controller.activate()
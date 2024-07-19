import asyncio
import ipaddress
from src.config_manager import ConfigManager
from src.relay_controller import RelayController
from src.logger import setup_logger

logger = setup_logger(__name__)

class IPScanner:
    def __init__(self, config: ConfigManager, relay_controller: RelayController):
        self.config = config
        self.relay_controller = relay_controller
        self.is_running = False

    async def start_monitoring(self):
        self.is_running = True
        while self.is_running:
            await self.scan_ips()
            await asyncio.sleep(self.config.scan_interval.success)

    async def stop_monitoring(self):
        self.is_running = False

    async def scan_ips(self):
        tasks = []
        ip_range = self.get_ip_range()
        all_ips = set(ip_range + self.config.whitelist)

        for ip in all_ips:
            if str(ip) not in self.config.passlist:
                tasks.append(self.check_ip(str(ip)))

        await asyncio.gather(*tasks)

    def get_ip_range(self):
        start_ip = ipaddress.ip_address(self.config.ip_range.start)
        end_ip = ipaddress.ip_address(self.config.ip_range.end)
        return [ipaddress.ip_address(ip) for ip in range(int(start_ip), int(end_ip) + 1)]

    async def check_ip(self, ip: str):
        for attempt in range(1, self.config.retry_config.count + 1):
            if await self.ping(ip):
                logger.info(f"IP {ip} is reachable (attempt {attempt})")
                return
            logger.warning(f"IP {ip} is unreachable (attempt {attempt})")
            await asyncio.sleep(self.config.retry_config.delay)
        
        logger.error(f"IP {ip} is unreachable after {self.config.retry_config.count} attempts")
        await self.relay_controller.activate()
        await asyncio.sleep(self.config.scan_interval.failure)

    async def ping(self, ip: str):
        try:
            proc = await asyncio.create_subprocess_exec(
                'ping', '-c', '1', '-W', '1', ip,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL
            )
            await proc.communicate()
            return proc.returncode == 0
        except Exception as e:
            logger.error(f"Error pinging {ip}: {e}")
            return False
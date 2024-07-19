import logging
import time
from threading import Thread
from queue import Queue
from ip_monitor.ping import ping_ip
from ip_monitor.relay import Relay
from ip_monitor.config import Config

class IPMonitor:
    def __init__(self, config: Config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.relay = Relay(config.gpio.relay_pin)
        self.ips_to_monitor = self._get_ips_to_monitor()

    def _get_ips_to_monitor(self):
        start_ip = int(self.config.ip_range.start)
        end_ip = int(self.config.ip_range.end)
        ip_range = [f"{i}.{j}.{k}.{l}" for i in range((start_ip >> 24) & 255, ((end_ip >> 24) & 255) + 1)
                    for j in range((start_ip >> 16) & 255, ((end_ip >> 16) & 255) + 1)
                    for k in range((start_ip >> 8) & 255, ((end_ip >> 8) & 255) + 1)
                    for l in range(start_ip & 255, (end_ip & 255) + 1)]
        return set(ip for ip in ip_range if ip not in self.config.passlist) | set(self.config.whitelist)

    def start(self):
        while True:
            self._monitor_ips()
            time.sleep(self.config.scan_interval.normal)

    def _monitor_ips(self):
        queue = Queue()
        threads = []

        for ip in self.ips_to_monitor:
            thread = Thread(target=self._check_ip, args=(ip, queue))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        while not queue.empty():
            ip, is_up = queue.get()
            if not is_up:
                self._handle_down_ip(ip)

    def _check_ip(self, ip, queue):
        is_up = ping_ip(ip)
        queue.put((ip, is_up))

    def _handle_down_ip(self, ip):
        self.logger.warning(f"IP {ip} is down. Retrying...")
        for _ in range(self.config.retry.count):
            time.sleep(self.config.retry.delay)
            if ping_ip(ip):
                self.logger.info(f"IP {ip} is back up after retry.")
                return

        self.logger.error(f"IP {ip} is still down after {self.config.retry.count} retries. Activating relay.")
        self.relay.activate()
        time.sleep(self.config.scan_interval.after_activation)
        self.relay.deactivate()
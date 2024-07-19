import time
from ping3 import ping
from gpio_controller import GPIOController

class PingMonitor:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.gpio = GPIOController(config['gpio_pin'], logger)

    def ip_range(self):
        start = list(map(int, self.config['ip_range']['start'].split('.')))
        end = list(map(int, self.config['ip_range']['end'].split('.')))
        for i in range(start[0], end[0] + 1):
            for j in range(start[1], end[1] + 1):
                for k in range(start[2], end[2] + 1):
                    for l in range(start[3], end[3] + 1):
                        yield f"{i}.{j}.{k}.{l}"

    def ping_ip(self, ip):
        for attempt in range(self.config['retry_attempts']):
            if ping(ip):
                return True
            time.sleep(self.config['retry_interval'])
        return False

    def run(self):
        self.logger.info("Starting network monitoring...")
        while True:
            all_ips_responsive = True
            for ip in self.ip_range():
                if ip in self.config['passlist']:
                    continue
                if not self.ping_ip(ip):
                    self.logger.warning(f"IP {ip} is not responsive")
                    all_ips_responsive = False

            for ip in self.config['whitelist']:
                if not self.ping_ip(ip):
                    self.logger.warning(f"Whitelisted IP {ip} is not responsive")
                    all_ips_responsive = False

            if not all_ips_responsive:
                self.gpio.activate()
            else:
                self.gpio.deactivate()

            self.logger.info(f"Sleeping for {self.config['iteration_interval']} seconds before next iteration")
            time.sleep(self.config['iteration_interval'])

    def cleanup(self):
        self.gpio.cleanup()
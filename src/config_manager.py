import yaml
from pydantic import BaseModel, IPvAnyAddress
from typing import List
import logging

logger = logging.getLogger(__name__)

class PingConfig(BaseModel):
    interval: int
    retry: dict

class Config(BaseModel):
    ip_range: dict
    whitelist: List[IPvAnyAddress]
    passlist: List[IPvAnyAddress]
    ping: PingConfig
    relay: dict

class ConfigManager:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self) -> Config:
        try:
            with open(self.config_path, 'r') as file:
                config_dict = yaml.safe_load(file)
            return Config(**config_dict)
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            raise

    @property
    def ip_range(self) -> tuple:
        return self.config.ip_range['start'], self.config.ip_range['end']

    @property
    def whitelist(self) -> List[IPvAnyAddress]:
        return self.config.whitelist

    @property
    def passlist(self) -> List[IPvAnyAddress]:
        return self.config.passlist

    @property
    def ping_interval(self) -> int:
        return self.config.ping.interval

    @property
    def retry_count(self) -> int:
        return self.config.ping.retry['count']

    @property
    def retry_delay(self) -> int:
        return self.config.ping.retry['delay']

    @property
    def relay_pin(self) -> int:
        return self.config.relay['pin']
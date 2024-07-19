from pydantic import BaseModel, IPvAnyAddress
from typing import List
import yaml

class IPRange(BaseModel):
    start: IPvAnyAddress
    end: IPvAnyAddress

class ScanInterval(BaseModel):
    success: int
    failure: int

class RetryConfig(BaseModel):
    count: int
    delay: int

class Config(BaseModel):
    ip_range: IPRange
    passlist: List[IPvAnyAddress]
    whitelist: List[IPvAnyAddress]
    relay: dict
    scan_interval: ScanInterval
    retry: RetryConfig

class ConfigManager:
    def __init__(self, config_path: str):
        with open(config_path, 'r') as file:
            config_dict = yaml.safe_load(file)
        self.config = Config(**config_dict)

    @property
    def ip_range(self) -> IPRange:
        return self.config.ip_range

    @property
    def passlist(self) -> List[IPvAnyAddress]:
        return self.config.passlist

    @property
    def whitelist(self) -> List[IPvAnyAddress]:
        return self.config.whitelist

    @property
    def relay_pin(self) -> int:
        return self.config.relay['pin']

    @property
    def scan_interval(self) -> ScanInterval:
        return self.config.scan_interval

    @property
    def retry_config(self) -> RetryConfig:
        return self.config.retry
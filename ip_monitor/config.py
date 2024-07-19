from pydantic import BaseModel, IPvAnyAddress
import yaml

class IPRange(BaseModel):
    start: IPvAnyAddress
    end: IPvAnyAddress

class RetryConfig(BaseModel):
    count: int
    delay: int

class ScanInterval(BaseModel):
    normal: int
    after_activation: int

class GPIOConfig(BaseModel):
    relay_pin: int

class LoggingConfig(BaseModel):
    level: str
    file: str

class Config(BaseModel):
    ip_range: IPRange
    passlist: list[IPvAnyAddress]
    whitelist: list[IPvAnyAddress]
    retry: RetryConfig
    scan_interval: ScanInterval
    gpio: GPIOConfig
    logging: LoggingConfig

def load_config(config_path: str = 'config.yml') -> Config:
    with open(config_path, 'r') as f:
        config_dict = yaml.safe_load(f)
    return Config(**config_dict)
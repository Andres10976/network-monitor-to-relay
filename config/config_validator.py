from pydantic import BaseModel, IPvAnyAddress, Field
from typing import List, Annotated

class IPRange(BaseModel):
    start: IPvAnyAddress
    end: IPvAnyAddress
    pin: Annotated[int, Field(ge=0, le=27)]

class WhitelistEntry(BaseModel):
    ip: IPvAnyAddress
    pin: Annotated[int, Field(ge=0, le=27)]

class PingConfig(BaseModel):
    timeout: float
    count: int
    interval: float

class ReconnectConfig(BaseModel):
    attempts: int
    interval: int

class CycleInterval(BaseModel):
    normal: int
    alert: int

class Config(BaseModel):
    ip_ranges: Annotated[List[IPRange], Field(min_items=1)]
    whitelist: List[WhitelistEntry]
    passlist: List[IPvAnyAddress]
    ping: PingConfig
    reconnect: ReconnectConfig
    cycle_interval: CycleInterval
    max_threads: int

def validate_config(config_dict: dict) -> Config:
    return Config(**config_dict)
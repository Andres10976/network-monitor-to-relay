import subprocess
import logging
from typing import List

logger = logging.getLogger(__name__)

def ping(ip: str, count: int, timeout: float, interval: float) -> bool:
    try:
        subprocess.check_output([
            "ping", "-c", str(count), 
            "-W", str(timeout), 
            "-i", str(interval),
            "-q", str(ip)
        ], stderr=subprocess.STDOUT)
        logger.debug(f"IP {ip} is reachable")
        return True
    except subprocess.CalledProcessError:
        logger.warning(f"IP {ip} is unreachable")
        return False
    except Exception as e:
        logger.error(f"Error while pinging {ip}: {e}")
        return False

def ping_with_retry(ip: str, ping_config: dict, reconnect_config: dict) -> bool:
    for attempt in range(reconnect_config['attempts']):
        if ping(ip, **ping_config):
            return True
        logger.info(f"Retrying {ip}, attempt {attempt + 1}/{reconnect_config['attempts']}")
    return False

def ping_all(ip_list: List[str], ping_config: dict, reconnect_config: dict) -> List[str]:
    unreachable_ips = []
    for ip in ip_list:
        if not ping_with_retry(ip, ping_config, reconnect_config):
            unreachable_ips.append(ip)
    return unreachable_ips
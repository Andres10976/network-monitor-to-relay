import subprocess
import logging

logger = logging.getLogger(__name__)

def ping_ip(ip: str) -> bool:
    try:
        result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        logger.error(f"Error pinging {ip}: {e}")
        return False
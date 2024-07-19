import asyncio
import logging

logger = logging.getLogger(__name__)

async def ping_ip(ip: str) -> bool:
    try:
        proc = await asyncio.create_subprocess_exec(
            'ping', '-c', '1', '-W', '1', ip,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL
        )
        await proc.wait()
        return proc.returncode == 0
    except Exception as e:
        logger.error(f"Error pinging {ip}: {e}")
        return False
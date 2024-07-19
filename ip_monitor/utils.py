import ipaddress

def ip_to_int(ip: str) -> int:
    return int(ipaddress.ip_address(ip))

def int_to_ip(ip_int: int) -> str:
    return str(ipaddress.ip_address(ip_int))

def is_ip_in_range(ip: str, start: str, end: str) -> bool:
    ip_int = ip_to_int(ip)
    start_int = ip_to_int(start)
    end_int = ip_to_int(end)
    return start_int <= ip_int <= end_int
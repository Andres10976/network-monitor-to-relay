import ipaddress
from typing import List, Dict

def get_ip_range(start_ip: str, end_ip: str) -> List[str]:
    start = ipaddress.IPv4Address(start_ip)
    end = ipaddress.IPv4Address(end_ip)
    return [str(ipaddress.IPv4Address(ip)) for ip in range(int(start), int(end) + 1)]

def get_all_ips(config: Dict) -> Dict[str, List[str]]:
    all_ips = {}
    for range_config in config['ip_ranges']:
        ips = get_ip_range(range_config['start'], range_config['end'])
        all_ips[range_config['pin']] = [ip for ip in ips if ip not in config['passlist']]
    
    for whitelist_entry in config['whitelist']:
        pin = whitelist_entry['pin']
        ip = whitelist_entry['ip']
        if pin in all_ips:
            all_ips[pin].append(ip)
        else:
            all_ips[pin] = [ip]
    
    return all_ips
import logging
import numpy as np

from ipaddress import ip_address, IPv4Address, IPv6Address
from typing import Optional

logger = logging.getLogger(__name__)


"""
Return random values for the different sections of ip addr
"""
# this mask is valid for the lifetime of the program
# we would want to save this to an actual lookup table in order to reverse the mask
# we would also need to keep the "algo" hidden
ip_masks = {i: str(np.random.randint(0, 256)) for i in range(256)}


"""
Self documenting code
Return a random pseudo-ip in string format
"""
def mask_ip(ip: (str or IPv4Address or IPv6Address)) -> Optional[str]:
    try:
        valid_ip = ip_address(ip)
    except ValueError:
        logger.error(f"Invalid IP address provided: {ip}")
        return None
    
    list_ip = valid_ip.exploded.split(".")
    return ".".join([ip_masks[int(addr)] for addr in list_ip])



def mask_device_id(device_id: str):
    return device_id


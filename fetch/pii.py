import logging
import numpy as np
import random
import string

from ipaddress import ip_address, IPv4Address, IPv6Address
from typing import Dict, Optional

logger = logging.getLogger(__name__)


"""
Return random values for the different sections of ip addr
"""
# this mask is valid for the lifetime of the program
# we would want to save this to an actual lookup table in order to reverse the mask
# we would also need to keep the "algo" hidden
ip_masks = {i: str(np.random.randint(0, 256)) for i in range(256)}


# this will be a quick & dirty implementation of a trie
# in real code I'd probably make a Trie class
device_id_masks = {}


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



def mask_device_id(device_id: str) -> Optional[str]:
    device_id_components = device_id.split("-")
    if len(device_id_components) != 3:
        logger.error(f"Improper device id provided: {device_id}")
        return None
    
    for idx, component_length in enumerate([3, 2, 4]):
        if component_length != len(device_id_components[idx]):
            logger.error(f"Improper device id provided: {device_id}")
            return None

    return insert_device_id(device_id_masks, device_id)

def random_digits_size(size: int = 3) -> str:
    return "".join(random.choices(string.digits, k=size))

def random_device_id() -> str:
    return f"{random_digits_size(3)}-{random_digits_size(2)}-{random_digits_size(4)}"

"""
"""
def insert_device_id(root: Dict[str, str], device_id: str) -> str:
    data = root
    for letter in device_id:
        data = data.setdefault(letter, {})
    if not data.get("end", False):
        data["end"] = random_device_id()
    return data["end"]

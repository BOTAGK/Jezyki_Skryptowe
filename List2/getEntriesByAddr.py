import ipaddress

from utils.validateLog import validate_log

def get_entries_by_addr(log, addr):
    validate_log(log)

    if not isinstance(addr, str):
        raise TypeError(f"Address must be a string, but is {type(addr).__name__}")

    #walidacja ip
    if any(char.isdigit() for char in addr) and "." in addr:
        try:
            ipaddress.ip_address(addr)
        except ValueError:
            raise ValueError(f"Given address '{addr} seems to be ip , but has wrong format")

    if not log:
        return []

    return [entry for entry in log if entry.id_orig_h == addr or entry.host == addr]
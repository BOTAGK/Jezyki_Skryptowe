def get_most_active_session(log):
    if not isinstance(log, dict):
        raise TypeError("log musi byc slownikiem")

    most_active_uid = None
    max_requests = 0

    for uid, entries in log.items():
        if not isinstance(entries, list):
            raise TypeError("Sesja musi byc listą")

        num_requests = len(entries)
        if num_requests > max_requests:
            max_requests = num_requests
            most_active_uid = uid

    if most_active_uid is None:
        return None

    return most_active_uid, max_requests
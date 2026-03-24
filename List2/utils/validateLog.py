from List2.readLog import LogEntry


def validate_log(log: list) -> bool:
    if not isinstance(log, list):
        raise TypeError(f"Log musi być listą. Otrzymano: {type(log).__name__}")

    if not log:
        return True

    first_entry = log[0]
    if not isinstance(first_entry, LogEntry):
        raise TypeError(f"Elementy logu muszą być typu LogEntry. Otrzymano: {type(first_entry).__name__}")

    return True
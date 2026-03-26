from List2.readLog import LogEntry
from List2.utils.validateLog import validate_log

def get_failed_reads(log, merge=False) -> list[LogEntry] | tuple[list[LogEntry], list[LogEntry]]:
    validate_log(log)

    lower_bound_4xx = 400
    upper_bound_4xx = 500
    upper_bound_5xx = 600

    logs_4xx = []
    logs_5xx = []

    #jedno przejscie przez logi
    for entry in log:
        code = entry.status_code

        if code is None:
            continue

        if lower_bound_4xx <= code < upper_bound_4xx:
            logs_4xx.append(entry)
        elif upper_bound_4xx <= code < upper_bound_5xx:
            logs_5xx.append(entry)

    if merge:
        return logs_4xx + logs_5xx
    else:
        return logs_4xx, logs_5xx
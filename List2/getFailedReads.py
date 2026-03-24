from utils.validateLog import validate_log

def get_failed_reads(log, merge=False):
    validate_log(log)

    logs_4xx = []
    logs_5xx = []

    #jedno przejscie przez logi
    for entry in log:
        code = entry.status_code

        if code is None:
            continue

        if 400 <= code < 500:
            logs_4xx.append(entry)
        elif 500 <= code < 600:
            logs_5xx.append(entry)

    if merge:
        return logs_4xx + logs_5xx
    else:
        return logs_4xx, logs_5xx
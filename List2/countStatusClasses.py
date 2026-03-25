from List2.utils.validateLog import validate_log


def count_status_classes(log):
    validate_log(log)

    counts = {}

    for entry in log:
        status_code = entry.status_code
        if status_code:
            code_class = f"{int(status_code / 100)}xx" #zmiana inta na string żeby uzyskać wymaganą nazwę grupy
            counts[code_class] = counts.get(code_class, 0) + 1

    return counts
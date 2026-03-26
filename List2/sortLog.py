from operator import attrgetter
from List2.utils.validateLog import validate_log

def sort_log(log, index, reverse=False):
    validate_log(log)
    if not log:
        return []

    if index < 0 or index >= len(log[0]):
        raise IndexError(f"Nieprawidłowy index: {index}.")

    return sorted(log, key = lambda x: x[index], reverse=reverse)


def sort_log_by_name(log, field_name, reverse=False):
    validate_log(log)
    if not log:
        return []

    if not hasattr(log[0], field_name):
        raise AttributeError(f"Błąd: Pole '{field_name}' nie istnieje w LogEntry")

    return sorted(log, key = attrgetter(field_name), reverse=reverse)
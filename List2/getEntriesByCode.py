from List2.utils.validateLog import validate_log

def get_entries_by_code(log, code):
    validate_log(log)

    if not isinstance(code, int):
        raise TypeError(f"Status code musi być int, ale jest: {type(code).__name__}")

    if not log:
        return []

    #zwracamy liste logow z takim codem
    return [entry for entry in log if entry.status_code == code]
from datetime import datetime, timezone

from List2.utils.validateLog import validate_log


def _ensure_datetime(val):

    if isinstance(val, datetime):
        return val

    try:

        return datetime.fromtimestamp(float(val), tz=timezone.utc)
    except (ValueError, TypeError):
        raise TypeError(
            f"Nie można przekonwertować '{val}' na datetime. "
            f"Oczekiwano obiektu datetime lub liczby (UNIX timestamp)."
        )

def get_entries_in_time_range(log, start, end):
    validate_log(log)

    if not log:
        return []

    start_dt = _ensure_datetime(start)
    end_dt = _ensure_datetime(end)

    return [entry for entry in log if start_dt <= entry.ts < end_dt]
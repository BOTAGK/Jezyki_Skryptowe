from collections import Counter
from List2.utils.validateLog import validate_log

def count_by_method(log) -> dict[str, int]:
    validate_log(log)

    return dict(Counter(e.method for e in log if e.method and e.method != "-"))

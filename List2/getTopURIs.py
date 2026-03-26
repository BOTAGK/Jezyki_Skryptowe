from List2.utils.validateLog import validate_log
from collections import Counter

def get_top_uris(log, n=10):
    validate_log(log)

    if not isinstance(n, int) or n < 0:
        raise TypeError("n musi byc dodatnia liczba całkowita")

    if not log:
        return []

    counts = Counter(entry.uri for entry in log)

    return counts.most_common(n)
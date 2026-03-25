from collections import Counter
from List2.utils.validateLog import validate_log


def get_top_ips(log, n=10) -> list[tuple]:
    validate_log(log)

    if not log:
        return []

    counts = Counter()

    for entry in log:
        counts[entry.id_orig_h] += 1

    return counts.most_common(n)
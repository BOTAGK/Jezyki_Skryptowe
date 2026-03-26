from List2.utils.validateLog import validate_log
from collections import Counter

def get_most_active_session(log):
    validate_log(log)

    if not log:
        return None

    uid_counts = Counter(entry.uid for entry in log)

    most_active_uid, max_request = uid_counts.most_common(1)[0]

    return most_active_uid, max_request
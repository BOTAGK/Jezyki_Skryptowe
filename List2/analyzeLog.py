from List2.utils.validateLog import validate_log
from collections import Counter

ERROR_CLASSES =(4,5)

def analyze_log(log):
    validate_log(log)

    if not log:
        return {
            'most_used_ip': None,
            'most_used_uri': None,
            'method_distribution': {},
            'error_count': 0,
            'total_requests': 0
        }

    ip_counter = Counter()
    uri_couner = Counter()
    method_counter = Counter()
    error_count = 0

    for entry in log:
        ip_counter[entry.id_orig_h] += 1
        uri_couner[entry.uri] += 1
        method_counter[entry.method] += 1

        status_code = entry.status_code
        if status_code is not None and (status_code // 100) in ERROR_CLASSES:
            error_count += 1

    return {
        'most_used_ip': ip_counter.most_common(1)[0],
        'most_used_uri': uri_couner.most_common(1)[0],
        'method_distribution': dict(method_counter),
        'error_count': error_count,
        'total_requests': len(log)
    }
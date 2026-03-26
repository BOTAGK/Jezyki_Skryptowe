from List2.utils.validateLog import validate_log


def analyze_log(log):
    validate_log(log)

    most_used_ip = {}
    most_used_uri = {}
    method_distribution = {}
    error_count = 0

    if not log:
        return {
            'most_used_ip': most_used_ip,
            'most_used_uri': most_used_uri,
            'method_distribution': method_distribution,
            'error_count': error_count,
            'total_requests': 0
        }

    for entry in log:
        entry_id = entry.id_orig_h
        most_used_ip[entry_id] = most_used_ip.get(entry_id, 0) + 1

        entry_uri = entry.uri
        most_used_uri[entry_uri] = most_used_uri.get(entry_uri, 0) + 1

        method = entry.method
        method_distribution[method] = method_distribution.get(method, 0) + 1

        status_code = entry.status_code
        if status_code is not None and status_code // 100 == (4 or 5):
            error_count += 1

    return {
        'most_used_ip': max(most_used_ip.items(), key=lambda item: item[1]),
        'most_used_uri': max(most_used_uri.items(), key=lambda item: item[1]),
        'method_distribution': method_distribution,
        'error_count': error_count,
        'total_requests': len(log)
    }
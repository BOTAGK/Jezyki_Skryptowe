from List2.utils.validateLog import validate_log


def detect_sus(log, threshold):
    validate_log(log)

    if not isinstance(threshold, int) or threshold <= 0:
        raise TypeError('Threshold musi byc dodatnia liczba calkowita')

    if not log:
        return {}

    by_ip = {}

    for entry in log:
        ip = entry.id_orig_h

        if ip not in by_ip:
            by_ip[ip] = {
                'requests': 0,
                'errors_404': 0,
                'short_intervals': 0,
                'last_ts': None
            }

        stats = by_ip[ip]
        stats['requests'] += 1

        if entry.status_code == 404:
            stats['errors_404'] += 1

        if stats['last_ts'] is not None:
            delta_seconds = (entry.ts - stats['last_ts']).total_seconds()
            
            if 0 <= delta_seconds <= 1:
                stats['short_intervals'] += 1

        stats['last_ts'] = entry.ts

    suspicious = {}

    for ip, stats in by_ip.items():
        is_high_requests = stats['requests'] >= threshold
        is_high_404 = stats['errors_404'] >= max(1, threshold // 3)
        is_many_short_gaps = stats['short_intervals'] >= max(1, threshold // 2)

        if is_high_requests and (is_high_404 or is_many_short_gaps):
            suspicious[ip] = {
                'requests': stats['requests'],
                'errors_404': stats['errors_404'],
                'short_intervals': stats['short_intervals']
            }

    return suspicious

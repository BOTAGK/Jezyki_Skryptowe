from List2.utils.validateLog import validate_log

def _init_ip_stats():
    return {
        "requests": 0,
        "errors_404": 0,
        "short_intervals": 0,
        "last_ts": None
    }


def _collect_ip_stats(log):
    ip_stats = {}

    for entry in log:
        ip = entry.id_orig_h

        if ip not in ip_stats:
            ip_stats[ip] = _init_ip_stats()

        stats = ip_stats[ip]
        stats["requests"] += 1

        if entry.status_code == 404:
            stats["errors_404"] += 1

        # liczenie krótkich odstępów czasu
        if stats["last_ts"] is not None:
            time_diff = (entry.ts - stats["last_ts"]).total_seconds()
            if 0 <= time_diff <= 1:
                stats["short_intervals"] += 1

        stats["last_ts"] = entry.ts
    return ip_stats

def _is_suspicious(stats, rq_threshold, error_percentage=0.33, intervals_percentage=0.5):
    is_heavy_traffic = stats["requests"] >= rq_threshold
    has_many_errors = stats["errors_404"] >= max(1, error_percentage * rq_threshold)
    has_many_short_intervals = stats["short_intervals"] >= max(1, intervals_percentage * rq_threshold)

    return is_heavy_traffic and (has_many_errors or has_many_short_intervals)

def detect_sus(log, threshold):
    validate_log(log)

    if not isinstance(threshold, int) or threshold <= 0:
        raise ValueError("Threshold musi być dodatnią liczbą całkowitą")

    if not log:
        return {}

    all_ip_stats = _collect_ip_stats(log)

    suspicious_ips = {}

    for ip, stats in all_ip_stats.items():
        if _is_suspicious(stats, threshold):
            suspicious_ips[ip] = {
                "requests": stats["requests"],
                "errors_404": stats["errors_404"],
                "short_intervals": stats["short_intervals"]
            }

    return suspicious_ips

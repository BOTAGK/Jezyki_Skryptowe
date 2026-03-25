def print_dict_entry_dates(log_dict):
    if not isinstance(log_dict, dict):
        raise TypeError("log_dict musi byc slownikiem")

    for uid in log_dict:
        entries = log_dict[uid]

        if not isinstance(entries, list):
            raise TypeError("Sesja musi byc listą")

        total_requests = len(entries)
        if total_requests == 0:
            continue

        session_ips = []
        session_hosts = []
        method_counts = {}
        timestamps = []
        code_2xx_count = 0

        for entry in entries:
            session_ips.append(entry['id_orig_h'])
            session_hosts.append(entry['host'])
            method_counts[entry['method']] = method_counts.get(entry['method'], 0) + 1
            timestamps.append(entry['ts'])

            if entry['status_code'] is not None and entry['status_code'] / 100 == 2:
                code_2xx_count += 1

        print(f"=== Session: {uid} ===")
        print(f"IP Addresses: {', '.join(session_ips)}")
        print(f"Hosts: {', '.join(session_hosts)}")
        print(f"Number of requests: {total_requests}")
        print(f"First/Last: {min(timestamps)} / {max(timestamps)}")
        print("HTTP Methods distribution:")
        for m, count in method_counts.items():
            print(f"  - {m}: {(count / total_requests) * 100:.2f}%")
        print(f"Ratio 2xx: {(code_2xx_count / total_requests):.2f}")
        print("-" * 20)


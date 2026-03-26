from collections import Counter

def print_dict_entry_dates(log_dict):

    if not isinstance(log_dict, dict):
        raise TypeError("log_dict musi byc slownikiem")

    for uid, entries in log_dict.items():
        total_requests = len(entries)

        if total_requests == 0:
            continue

        #set usuwa powtarzajace sie ip i hostname
        ips = set()
        hosts = set()
        timestamps = []
        methods_counter = Counter()
        success_codes_count = 0

        for entry in entries:
            ips.add(entry["id_orig_h"])
            hosts.add(entry["host"])
            timestamps.append(entry["ts"])
            methods_counter[entry["method"]] += 1

            #bezpieczne sprawdzenie kodu 2xx
            code = entry.get("status_code")
            if code is not None and code // 100 == 2:
                success_codes_count += 1

        first_request = min(timestamps)
        last_request = max(timestamps)
        ratio_2xx = success_codes_count / total_requests

        print(f" Sesja (UID): {uid}")
        print(f"   ➔ Adresy IP: {', '.join(ips)}")
        print(f"   ➔ Hosty: {', '.join(hosts)}")
        print(f"   ➔ Liczba żądań: {total_requests}")
        print(f"   ➔ Czas trwania: od {first_request} do {last_request}")
        print(f"   ➔ Stosunek kodów 2xx: {ratio_2xx:.2f} ({success_codes_count}/{total_requests})")

        print("   ➔ Podział metod HTTP:")
        for method, count in methods_counter.items():
            percentage = (count / total_requests) * 100
            print(f"      • {method}: {percentage:.1f}%")

        print("-" * 40)


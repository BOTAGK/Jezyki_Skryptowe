import sys
from datetime import datetime, timezone

from common import run_safely, echo

def read_log(process_item):
    def print_formatted_item(item):
        print(process_item(item))

    tuples_list = process_to_list()

    # test wyswietlania
    # for i in range(0, 20):
    #     print_formatted_item(tuples_list[i])
    #     print()

    for log in tuples_list:
        print_formatted_item(log)

def process_to_list():
    tuples_list = []

    for line in get_line():
        try:
            log_tuple = process_to_tuple(line)
            tuples_list.append(log_tuple)
        except (ValueError, EOFError) as e:
            print(f"Error processing line: {e}")

    return tuples_list

def get_line():
    has_data = False

    while line := sys.stdin.readline():
        has_data = True
        yield line

    if not has_data:
        raise EOFError("Błąd: Strumień wejściowy jest pusty.")

def process_to_tuple(log_line):
    parts = log_line.split('\t')

    if len(parts) < 3:
        raise ValueError(f"Nieprawidłowy format logu: {log_line}")

    timestamp = datetime.fromtimestamp(float(parts[0]), tz=timezone.utc).isoformat()
    uid = parts[1]
    id_orig_h = parts[2]
    id_orig_p = int(parts[3])
    id_resp_h = parts[4]
    id_resp_p = int(parts[5])
    method = parts[7]
    host = parts[8]
    uri = parts[9]

    if parts[14] != "-":
        status_code = int(parts[14])
        status_text = parts[15]
    else:
        status_code = '-'
        status_text = '-'


    return (timestamp, uid, id_orig_h, id_orig_p, id_resp_h, id_resp_p, method, host, uri, status_code, status_text)


if __name__ == "__main__":
    run_safely(lambda: read_log(echo))
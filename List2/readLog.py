import sys
import logging
from datetime import datetime, timezone
from typing import Optional

from List2.strucutres import LogEntry

IDX_TS = 0
IDX_UID = 1
IDX_ORIG_H = 2
IDX_ORIG_P = 3
IDX_RESP_H = 4
IDX_RESP_P = 5
IDX_METHOD = 7
IDX_HOST = 8
IDX_URI = 9
IDX_STATUS_CODE = 14
IDX_STATUS_TEXT = 15

MIN_PARTS_LENGTH = 15


def parse_log_line(line: str) -> Optional[LogEntry]:
    #jedna linia logu na obiekt LogEntry
    line = line.strip()
    if not line or line.startswith('#'):
        return None

    parts = line.split('\t')

    #potrzebujemy conajmniej 14 indeksu
    if len(parts) < MIN_PARTS_LENGTH:
        logging.warning(f"Nieprawidłowy format linii (zbyt mało kolumn: {line[:50]}...")
        return None

    try:
        #konwersja znacznikow czasowych na datetime
        ts = datetime.fromtimestamp(float(parts[IDX_TS]), tz=timezone.utc)

        status_code = int(parts[IDX_STATUS_CODE]) if parts[IDX_STATUS_CODE] != "-" else None

        status_text = parts[IDX_STATUS_TEXT] if len(parts) > IDX_STATUS_TEXT and parts[IDX_STATUS_TEXT] != "-" else None

        return LogEntry(
            ts = ts,
            uid = parts[IDX_UID],
            id_orig_h = parts[IDX_ORIG_H],
            id_orig_p = int(parts[IDX_ORIG_P]),
            id_resp_h = parts[IDX_RESP_H],
            id_resp_p = int(parts[IDX_RESP_P]),
            method = parts[IDX_METHOD],
            host = parts[IDX_HOST],
            uri = parts[IDX_URI],
            status_code = status_code,
            status_text = status_text
        )
    except (ValueError, IndexError) as e:
        logging.error(f"Błąd konwersji danych w linii: {e} | linia: {line[:50]}...")
        return None

def read_log(stream=sys.stdin) -> list[LogEntry]:
    tuples_list = []

    for line in stream:
        entry = parse_log_line(line)
        if entry is not None:
            tuples_list.append(entry)

    return tuples_list


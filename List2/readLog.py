import sys
import logging
from datetime import datetime, timezone
from typing import NamedTuple, Optional
from common import run_safely


class LogEntry(NamedTuple):
    ts: datetime
    uid: str
    id_orig_h: str
    id_orig_p: int
    id_resp_h: str
    id_resp_p: int
    method: str
    host: str
    uri: str
    status_code: Optional[int]
    status_text: Optional[str]

def parse_log_line(line: str) -> Optional[LogEntry]:

    #jedna linia logu na obiekt LogEntry
    line = line.strip()

    if not line or line.startswith('#'):
        return None

    parts = line.split('\t')

    #potrzebujemy conajmniej 14 indeksu
    if len(parts) < 15:
        logging.warning(f"Nieprawidłowy format linii (zbyt mało kolumn: {line[:50]}...")
        return None

    try:
        #konwersja znacznikow czasowych na datetime
        ts = datetime.fromtimestamp(float(parts[0]), tz=timezone.utc)

        status_code = int(parts[14]) if parts[14] != "-" else None

        status_text = parts[15] if len(parts) > 15 and parts[15] != "-" else None

        return LogEntry(
            ts = ts,
            uid = parts[1],
            id_orig_h=parts[2],
            id_orig_p=int(parts[3]),
            id_resp_h=parts[4],
            id_resp_p=int(parts[5]),
            method=parts[7],
            host=parts[8],
            uri=parts[9],
            status_code=status_code,
            status_text=status_text
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


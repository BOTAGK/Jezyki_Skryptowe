from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time, timezone
from pathlib import Path
from typing import Iterator, Optional

from List2.readLog import parse_log_line
from List2.strucutres import LogEntry


@dataclass(frozen=True)
class LogRecord:
    entry: LogEntry
    raw: str


def stream_log_file(file_path: Path, max_lines: Optional[int] = None) -> Iterator[LogRecord]:
    count = 0

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            entry = parse_log_line(line)
            if entry is None:
                continue

            yield LogRecord(entry=entry, raw=line.rstrip("\n"))

            count += 1
            if max_lines is not None and count >= max_lines:
                break


class LogStore:
    def __init__(self) -> None:
        self.records: list[LogRecord] = []
        self.filtered_indices: list[int] = []

    def clear(self) -> None:
        self.records.clear()
        self.filtered_indices.clear()

    def append_records(self, records: list[LogRecord]) -> None:
        start = len(self.records)
        self.records.extend(records)
        self.filtered_indices.extend(range(start, start + len(records)))

    def filtered_count(self) -> int:
        return len(self.filtered_indices)

    def record_at(self, row: int) -> LogRecord:
        return self.records[self.filtered_indices[row]]

    def apply_filter(self, start_dt: Optional[datetime], end_dt: Optional[datetime]) -> None:
        self.filtered_indices = filter_indices_by_datetime(self.records, start_dt, end_dt)


def parse_log_file(file_path: Path, max_lines: Optional[int] = None) -> list[LogRecord]:
    records: list[LogRecord] = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            entry = parse_log_line(line)
            if entry is None:
                continue

            records.append(LogRecord(entry=entry, raw=line.rstrip("\n")))

            if max_lines is not None and len(records) >= max_lines:
                break

    return records


def truncate_text(text: str, max_len: int = 30) -> str:
    if len(text) <= max_len:
        return text
    if max_len <= 3:
        return text[:max_len]
    return f"{text[:max_len - 3]}..."


def record_display_text(record: LogRecord, max_len: int = 30) -> str:
    entry = record.entry
    uri = truncate_text(entry.uri, max_len)
    timestamp = entry.ts.strftime("%d/%b/%Y:%H:%M:%S")
    return f'{entry.id_orig_h} - [{timestamp}] "{entry.method} {uri}"'


def filter_by_datetime(
    records: list[LogRecord],
    start_dt: Optional[datetime],
    end_dt: Optional[datetime],
) -> list[LogRecord]:
    return [records[index] for index in filter_indices_by_datetime(records, start_dt, end_dt)]


def filter_indices_by_datetime(
    records: list[LogRecord],
    start_dt: Optional[datetime],
    end_dt: Optional[datetime],
) -> list[int]:
    if start_dt is None and end_dt is None:
        return list(range(len(records)))

    filtered: list[int] = []
    for index, record in enumerate(records):
        ts = record.entry.ts
        if start_dt is not None and ts < start_dt:
            continue
        if end_dt is not None and ts > end_dt:
            continue
        filtered.append(index)

    return filtered


def parse_datetime_input(
    date_str: str,
    time_str: str,
    default_time: time,
) -> Optional[datetime]:
    date_str = date_str.strip()
    if not date_str:
        return None

    time_str = time_str.strip()
    parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()

    if time_str:
        parsed_time = datetime.strptime(time_str, "%H:%M:%S").time()
    else:
        parsed_time = default_time

    combined = datetime.combine(parsed_date, parsed_time)
    return combined.replace(tzinfo=timezone.utc)


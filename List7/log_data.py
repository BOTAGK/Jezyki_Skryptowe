from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time, timezone
from pathlib import Path
from typing import Optional

from List2.readLog import parse_log_line
from List2.strucutres import LogEntry


@dataclass(frozen=True)
class LogRecord:
    entry: LogEntry
    raw: str


class LogStore:
    def __init__(self) -> None:
        self.records: list[LogRecord] = []
        self.filtered: list[LogRecord] = []

    def load(self, file_path: Path) -> None:
        self.records = parse_log_file(file_path)
        self.filtered = list(self.records)

    def apply_filter(self, start_dt: Optional[datetime], end_dt: Optional[datetime]) -> None:
        self.filtered = filter_by_datetime(self.records, start_dt, end_dt)


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
    if start_dt is None and end_dt is None:
        return list(records)

    filtered: list[LogRecord] = []
    for record in records:
        ts = record.entry.ts
        if start_dt is not None and ts < start_dt:
            continue
        if end_dt is not None and ts > end_dt:
            continue
        filtered.append(record)

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


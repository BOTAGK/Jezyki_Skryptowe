from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time, timezone
from pathlib import Path
from typing import Callable, Iterator, Optional

from List2.readLog import parse_log_line
from List2.strucutres import LogEntry


@dataclass(frozen=True)
class LogRecord:
    entry: LogEntry
    raw: str


LogFilter = Callable[[LogRecord], bool]


def apply_log_filters(
    records: list[LogRecord],
    filters: list[LogFilter],
) -> list[int]:
    filtered: list[int] = []

    for index, record in enumerate(records):
        if all(log_filter(record) for log_filter in filters):
            filtered.append(index)

    return filtered


def _text_equals(value: Optional[str], expected: str, case_sensitive: bool = True) -> bool:
    if value is None:
        return False
    if case_sensitive:
        return value == expected
    return value.casefold() == expected.casefold()


def _text_contains(value: Optional[str], text: str, case_sensitive: bool = False) -> bool:
    if value is None:
        return False
    if case_sensitive:
        return text in value
    return text.casefold() in value.casefold()


def _number_in_range(value: int, min_value: Optional[int], max_value: Optional[int]) -> bool:
    if min_value is not None and value < min_value:
        return False
    if max_value is not None and value > max_value:
        return False
    return True


def timestamp_filter(timestamp: datetime) -> LogFilter:
    def matches(record: LogRecord) -> bool:
        return record.entry.ts == timestamp

    return matches


def date_range_filter(
    start_dt: Optional[datetime],
    end_dt: Optional[datetime],
) -> LogFilter:
    def matches(record: LogRecord) -> bool:
        ts = record.entry.ts
        if start_dt is not None and ts < start_dt:
            return False
        if end_dt is not None and ts > end_dt:
            return False
        return True

    return matches


def uid_filter(uid: str, case_sensitive: bool = True) -> LogFilter:
    def matches(record: LogRecord) -> bool:
        return _text_equals(record.entry.uid, uid, case_sensitive)

    return matches


def uid_contains_filter(text: str, case_sensitive: bool = False) -> LogFilter:
    def matches(record: LogRecord) -> bool:
        return _text_contains(record.entry.uid, text, case_sensitive)

    return matches


def orig_host_filter(host: str, case_sensitive: bool = True) -> LogFilter:
    def matches(record: LogRecord) -> bool:
        return _text_equals(record.entry.id_orig_h, host, case_sensitive)

    return matches


def orig_host_contains_filter(text: str, case_sensitive: bool = False) -> LogFilter:
    def matches(record: LogRecord) -> bool:
        return _text_contains(record.entry.id_orig_h, text, case_sensitive)

    return matches


def orig_port_filter(port: int) -> LogFilter:
    def matches(record: LogRecord) -> bool:
        return record.entry.id_orig_p == port

    return matches


def orig_port_range_filter(min_port: Optional[int], max_port: Optional[int]) -> LogFilter:
    def matches(record: LogRecord) -> bool:
        return _number_in_range(record.entry.id_orig_p, min_port, max_port)

    return matches


def resp_host_filter(host: str, case_sensitive: bool = True) -> LogFilter:
    def matches(record: LogRecord) -> bool:
        return _text_equals(record.entry.id_resp_h, host, case_sensitive)

    return matches


def resp_host_contains_filter(text: str, case_sensitive: bool = False) -> LogFilter:
    def matches(record: LogRecord) -> bool:
        return _text_contains(record.entry.id_resp_h, text, case_sensitive)

    return matches


def resp_port_filter(port: int) -> LogFilter:
    def matches(record: LogRecord) -> bool:
        return record.entry.id_resp_p == port

    return matches


def resp_port_range_filter(min_port: Optional[int], max_port: Optional[int]) -> LogFilter:
    def matches(record: LogRecord) -> bool:
        return _number_in_range(record.entry.id_resp_p, min_port, max_port)

    return matches


def method_filter(method: str, case_sensitive: bool = False) -> LogFilter:
    def matches(record: LogRecord) -> bool:
        return _text_equals(record.entry.method, method, case_sensitive)

    return matches


def host_filter(host: str, case_sensitive: bool = False) -> LogFilter:
    def matches(record: LogRecord) -> bool:
        return _text_equals(record.entry.host, host, case_sensitive)

    return matches


def host_contains_filter(text: str, case_sensitive: bool = False) -> LogFilter:
    def matches(record: LogRecord) -> bool:
        return _text_contains(record.entry.host, text, case_sensitive)

    return matches


def uri_filter(uri: str, case_sensitive: bool = True) -> LogFilter:
    def matches(record: LogRecord) -> bool:
        return _text_equals(record.entry.uri, uri, case_sensitive)

    return matches


def uri_contains_filter(text: str, case_sensitive: bool = False) -> LogFilter:
    def matches(record: LogRecord) -> bool:
        return _text_contains(record.entry.uri, text, case_sensitive)

    return matches


def status_code_filter(status_code: int) -> LogFilter:
    def matches(record: LogRecord) -> bool:
        status = record.entry.status_code
        return status == status_code

    return matches


def status_code_range_filter(min_code: Optional[int], max_code: Optional[int]) -> LogFilter:
    def matches(record: LogRecord) -> bool:
        status = record.entry.status_code
        return status is not None and _number_in_range(status, min_code, max_code)

    return matches


def status_class_filter(status_class: int) -> LogFilter:
    if status_class < 1 or status_class > 5:
        raise ValueError("Status class must be between 1 and 5.")

    def matches(record: LogRecord) -> bool:
        status = record.entry.status_code
        return status is not None and status // 100 == status_class

    return matches


def errors_only_filter() -> LogFilter:
    return status_code_range_filter(400, 599)

def no_error_only_filter() -> LogFilter:
    return status_code_range_filter(200, 399)


def status_text_filter(status_text: str, case_sensitive: bool = False) -> LogFilter:
    def matches(record: LogRecord) -> bool:
        return _text_equals(record.entry.status_text, status_text, case_sensitive)

    return matches


def status_text_contains_filter(text: str, case_sensitive: bool = False) -> LogFilter:
    def matches(record: LogRecord) -> bool:
        return _text_contains(record.entry.status_text, text, case_sensitive)

    return matches


def missing_status_code_filter() -> LogFilter:
    def matches(record: LogRecord) -> bool:
        return record.entry.status_code is None

    return matches


def missing_status_text_filter() -> LogFilter:
    def matches(record: LogRecord) -> bool:
        return record.entry.status_text is None

    return matches


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

    # def load(self, file_path: Path) -> None:
    #     self.clear()
    #     records = parse_log_file(file_path)
    #     self.append_records(records)    

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

    def apply_filters(self, filters: list[LogFilter]) -> None:
        self.filtered_indices = apply_log_filters(self.records, filters)

    def sort_filtered_by_datetime(self, descending: bool = False) -> None:
        self.filtered_indices = sort_indices_by_datetime(
            self.records,
            self.filtered_indices,
            descending,
        )  


# def parse_log_file(file_path: Path, max_lines: Optional[int] = None) -> list[LogRecord]:
#     records: list[LogRecord] = []

#     with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
#         for line in file:
#             entry = parse_log_line(line)
#             if entry is None:
#                 continue

#             records.append(LogRecord(entry=entry, raw=line.rstrip("\n")))

#             if max_lines is not None and len(records) >= max_lines:
#                 break

#     return records


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


def sort_indices_by_datetime(
    records: list[LogRecord],
    indices: list[int],
    descending: bool = False,
) -> list[int]:
    if not indices:
        return []

    def get_timestamp(index: int) -> datetime:
        return records[index].entry.ts

    sorted_indices = sorted(indices, key=get_timestamp, reverse=descending)

    return sorted_indices


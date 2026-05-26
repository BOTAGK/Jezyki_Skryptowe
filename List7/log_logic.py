from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from List2.readLog import read_log
from List2.strucutres import LogEntry


@dataclass
class LoadedLog:
    path: Path
    entries: list[LogEntry]


class LogService:
    def load_file(self, file_path: str | Path) -> LoadedLog:
        path = Path(file_path)

        with path.open("r", encoding="utf-8", errors="replace") as file:
            return LoadedLog(path, read_log(file))

    def filter_by_date(
        self,
        entries: list[LogEntry],
        start_date: date,
        end_date: date,
    ) -> list[LogEntry]:
        if start_date > end_date:
            raise ValueError("Data poczatkowa nie moze byc pozniejsza niz koncowa.")

        return [
            entry
            for entry in entries
            if start_date <= entry.ts.date() <= end_date
        ]

    def get_date_range(self, entries: list[LogEntry]) -> tuple[date, date]:
        dates = [entry.ts.date() for entry in entries]
        return min(dates), max(dates)

    def make_list_text(self, entry: LogEntry) -> str:
        uri = entry.uri[:30] + "..." if len(entry.uri) > 30 else entry.uri
        timestamp = entry.ts.strftime("%d/%b/%Y:%H:%M:%S %z")
        return f'{entry.id_orig_h} - [{timestamp}] "{entry.method} {uri}"'

    def get_timezone(self, entry: LogEntry) -> str:
        return entry.ts.strftime("%Z") or "UTC"

    def get_size(self, entry: LogEntry) -> str:
        return "-"

    def get_status_color(self, status_code: int | None) -> str:
        if status_code is None:
            return "lightgray"
        if 200 <= status_code < 300:
            return "#36e636"
        if 300 <= status_code < 400:
            return "#f2dc4d"
        if 400 <= status_code < 500:
            return "#ffad42"
        if 500 <= status_code < 600:
            return "#f25757"
        return "lightgray"

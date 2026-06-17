from __future__ import annotations

from datetime import date, datetime


def parse_gtfs_date(value: str | None) -> date | None:
    if value is None or value.strip() == "":
        return None
    return datetime.strptime(value.strip(), "%Y%m%d").date()


def parse_gtfs_time_to_seconds(value: str | None) -> int | None:
    if value is None or value.strip() == "":
        return None

    parts = value.strip().split(":")
    if len(parts) != 3:
        return None

    hours, minutes, seconds = (int(part) for part in parts)
    if not (0 <= minutes < 60 and 0 <= seconds < 60):
        return None
    return hours * 3600 + minutes * 60 + seconds


def format_gtfs_seconds(value: int | None) -> str | None:
    if value is None:
        return None
    hours = value // 3600
    minutes = (value % 3600) // 60
    seconds = value % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

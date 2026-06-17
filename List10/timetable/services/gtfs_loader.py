from __future__ import annotations

import csv
import io
import zipfile
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import Any

from sqlalchemy import delete, insert
from sqlalchemy.orm import Session

from timetable.models import Route, ServiceCalendar, Stop, StopTime, Trip
from timetable.schemas.gtfs import ImportSummary
from timetable.utils.time import parse_gtfs_date, parse_gtfs_time_to_seconds


RowMapper = Callable[[dict[str, str]], dict[str, Any]]


class GtfsLoader:
    required_files = {
        "stops.txt",
        "routes.txt",
        "calendar.txt",
        "trips.txt",
        "stop_times.txt",
    }

    def __init__(self, session: Session, batch_size: int = 5000) -> None:
        if batch_size <= 0:
            raise ValueError("batch_size must be positive")
        self.session = session
        self.batch_size = batch_size

    def load_zip(self, zip_path: str | Path, replace_existing: bool = False) -> ImportSummary:
        zip_path = Path(zip_path)
        if not zip_path.exists():
            raise FileNotFoundError(zip_path)

        with zipfile.ZipFile(zip_path) as archive:
            members = self._find_members(archive)
            missing = sorted(self.required_files - set(members))
            if missing:
                raise ValueError(f"Missing GTFS files: {', '.join(missing)}")

            if replace_existing:
                self._clear_existing_data()

            summary = ImportSummary()
            summary.stops = self._load_table(
                archive, members["stops.txt"], Stop, self._map_stop
            )
            summary.routes = self._load_table(
                archive, members["routes.txt"], Route, self._map_route
            )
            summary.service_calendar = self._load_table(
                archive,
                members["calendar.txt"],
                ServiceCalendar,
                self._map_calendar,
            )
            summary.trips = self._load_table(
                archive, members["trips.txt"], Trip, self._map_trip
            )
            summary.stop_times = self._load_table(
                archive,
                members["stop_times.txt"],
                StopTime,
                self._map_stop_time,
            )
            return summary

    def _find_members(self, archive: zipfile.ZipFile) -> dict[str, str]:
        members: dict[str, str] = {}
        for name in archive.namelist():
            basename = Path(name).name.lower()
            if basename in self.required_files:
                members[basename] = name
        return members

    def _clear_existing_data(self) -> None:
        self.session.execute(delete(StopTime))
        self.session.execute(delete(Trip))
        self.session.execute(delete(ServiceCalendar))
        self.session.execute(delete(Route))
        self.session.execute(delete(Stop))
        self.session.flush()

    def _load_table(
        self,
        archive: zipfile.ZipFile,
        member: str,
        model: type,
        mapper: RowMapper,
    ) -> int:
        count = 0
        batch: list[dict[str, Any]] = []

        for row in self._iter_rows(archive, member):
            batch.append(mapper(row))
            if len(batch) >= self.batch_size:
                count += self._insert_batch(model, batch)
                batch.clear()

        if batch:
            count += self._insert_batch(model, batch)

        return count

    def _insert_batch(self, model: type, batch: list[dict[str, Any]]) -> int:
        self.session.execute(insert(model), batch)
        self.session.flush()
        return len(batch)

    def _iter_rows(self, archive: zipfile.ZipFile, member: str) -> Iterator[dict[str, str]]:
        with archive.open(member) as raw:
            wrapper = io.TextIOWrapper(raw, encoding="utf-8-sig", newline="")
            reader = csv.DictReader(wrapper)
            for row in reader:
                yield {key.strip(): value for key, value in row.items() if key is not None}

    def _map_stop(self, row: dict[str, str]) -> dict[str, Any]:
        return {
            "stop_id": clean(row.get("stop_id")),
            "stop_code": clean(row.get("stop_code")),
            "stop_name": clean(row.get("stop_name")) or "",
            "stop_lat": parse_float(row.get("stop_lat")),
            "stop_lon": parse_float(row.get("stop_lon")),
        }

    def _map_route(self, row: dict[str, str]) -> dict[str, Any]:
        return {
            "route_id": clean(row.get("route_id")),
            "agency_id": clean(row.get("agency_id")),
            "route_short_name": clean(row.get("route_short_name")),
            "route_long_name": clean(row.get("route_long_name")),
            "route_desc": clean(row.get("route_desc")),
            "route_type": parse_int(row.get("route_type")),
        }

    def _map_calendar(self, row: dict[str, str]) -> dict[str, Any]:
        return {
            "service_id": clean(row.get("service_id")),
            "monday": parse_bool(row.get("monday")),
            "tuesday": parse_bool(row.get("tuesday")),
            "wednesday": parse_bool(row.get("wednesday")),
            "thursday": parse_bool(row.get("thursday")),
            "friday": parse_bool(row.get("friday")),
            "saturday": parse_bool(row.get("saturday")),
            "sunday": parse_bool(row.get("sunday")),
            "start_date": parse_gtfs_date(row.get("start_date")),
            "end_date": parse_gtfs_date(row.get("end_date")),
        }

    def _map_trip(self, row: dict[str, str]) -> dict[str, Any]:
        return {
            "route_id": clean(row.get("route_id")),
            "service_id": clean(row.get("service_id")),
            "trip_id": clean(row.get("trip_id")),
            "trip_headsign": clean(row.get("trip_headsign")),
            "direction_id": parse_int(row.get("direction_id")),
        }

    def _map_stop_time(self, row: dict[str, str]) -> dict[str, Any]:
        arrival_time = clean(row.get("arrival_time"))
        departure_time = clean(row.get("departure_time"))
        return {
            "trip_id": clean(row.get("trip_id")),
            "arrival_time": arrival_time,
            "departure_time": departure_time,
            "arrival_seconds": parse_gtfs_time_to_seconds(arrival_time),
            "departure_seconds": parse_gtfs_time_to_seconds(departure_time),
            "stop_id": clean(row.get("stop_id")),
            "stop_sequence": parse_int(row.get("stop_sequence")) or 0,
        }


def clean(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return value or None


def parse_int(value: str | None) -> int | None:
    value = clean(value)
    if value is None:
        return None
    return int(value)


def parse_float(value: str | None) -> float | None:
    value = clean(value)
    if value is None:
        return None
    return float(value)


def parse_bool(value: str | None) -> bool:
    return clean(value) == "1"

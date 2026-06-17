from __future__ import annotations

import csv
import io
import zipfile
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import Any

from sqlalchemy import delete, insert
from sqlalchemy.orm import Session

from timetable.constants import (
    DatabaseColumn,
    GtfsColumn,
    GtfsFile,
    GtfsValue,
    TextEncoding,
)
from timetable.models import Route, ServiceCalendar, Stop, StopTime, Trip
from timetable.schemas.gtfs import ImportSummary
from timetable.utils.time import parse_gtfs_date, parse_gtfs_time_to_seconds


RowMapper = Callable[[dict[str, str]], dict[str, Any]]


class GtfsLoader:
    required_files: set[GtfsFile] = set(GtfsFile)

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
            missing = sorted(file.value for file in self.required_files - set(members))
            if missing:
                raise ValueError(f"Missing GTFS files: {', '.join(missing)}")

            if replace_existing:
                self._clear_existing_data()

            summary = ImportSummary()
            summary.stops = self._load_table(
                archive, members[GtfsFile.STOPS], Stop, self._map_stop
            )
            summary.routes = self._load_table(
                archive, members[GtfsFile.ROUTES], Route, self._map_route
            )
            summary.service_calendar = self._load_table(
                archive,
                members[GtfsFile.CALENDAR],
                ServiceCalendar,
                self._map_calendar,
            )
            summary.trips = self._load_table(
                archive, members[GtfsFile.TRIPS], Trip, self._map_trip
            )
            summary.stop_times = self._load_table(
                archive,
                members[GtfsFile.STOP_TIMES],
                StopTime,
                self._map_stop_time,
            )
            return summary

    def _find_members(self, archive: zipfile.ZipFile) -> dict[GtfsFile, str]:
        members: dict[GtfsFile, str] = {}
        for name in archive.namelist():
            basename = Path(name).name.lower()
            try:
                gtfs_file = GtfsFile(basename)
            except ValueError:
                continue
            members[gtfs_file] = name
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
            wrapper = io.TextIOWrapper(
                raw,
                encoding=TextEncoding.UTF_8_SIG.value,
                newline="",
            )
            reader = csv.DictReader(wrapper)
            for row in reader:
                yield {key.strip(): value for key, value in row.items() if key is not None}

    def _map_stop(self, row: dict[str, str]) -> dict[str, Any]:
        return {
            DatabaseColumn.STOP_ID.value: clean(gtfs_field(row, GtfsColumn.STOP_ID)),
            DatabaseColumn.STOP_CODE.value: clean(gtfs_field(row, GtfsColumn.STOP_CODE)),
            DatabaseColumn.STOP_NAME.value: clean(gtfs_field(row, GtfsColumn.STOP_NAME)) or "",
            DatabaseColumn.STOP_LAT.value: parse_float(gtfs_field(row, GtfsColumn.STOP_LAT)),
            DatabaseColumn.STOP_LON.value: parse_float(gtfs_field(row, GtfsColumn.STOP_LON)),
        }

    def _map_route(self, row: dict[str, str]) -> dict[str, Any]:
        return {
            DatabaseColumn.ROUTE_ID.value: clean(gtfs_field(row, GtfsColumn.ROUTE_ID)),
            DatabaseColumn.AGENCY_ID.value: clean(gtfs_field(row, GtfsColumn.AGENCY_ID)),
            DatabaseColumn.ROUTE_SHORT_NAME.value: clean(
                gtfs_field(row, GtfsColumn.ROUTE_SHORT_NAME)
            ),
            DatabaseColumn.ROUTE_LONG_NAME.value: clean(
                gtfs_field(row, GtfsColumn.ROUTE_LONG_NAME)
            ),
            DatabaseColumn.ROUTE_DESC.value: clean(gtfs_field(row, GtfsColumn.ROUTE_DESC)),
            DatabaseColumn.ROUTE_TYPE.value: parse_int(gtfs_field(row, GtfsColumn.ROUTE_TYPE)),
        }

    def _map_calendar(self, row: dict[str, str]) -> dict[str, Any]:
        return {
            DatabaseColumn.SERVICE_ID.value: clean(gtfs_field(row, GtfsColumn.SERVICE_ID)),
            DatabaseColumn.MONDAY.value: parse_bool(gtfs_field(row, GtfsColumn.MONDAY)),
            DatabaseColumn.TUESDAY.value: parse_bool(gtfs_field(row, GtfsColumn.TUESDAY)),
            DatabaseColumn.WEDNESDAY.value: parse_bool(gtfs_field(row, GtfsColumn.WEDNESDAY)),
            DatabaseColumn.THURSDAY.value: parse_bool(gtfs_field(row, GtfsColumn.THURSDAY)),
            DatabaseColumn.FRIDAY.value: parse_bool(gtfs_field(row, GtfsColumn.FRIDAY)),
            DatabaseColumn.SATURDAY.value: parse_bool(gtfs_field(row, GtfsColumn.SATURDAY)),
            DatabaseColumn.SUNDAY.value: parse_bool(gtfs_field(row, GtfsColumn.SUNDAY)),
            DatabaseColumn.START_DATE.value: parse_gtfs_date(
                gtfs_field(row, GtfsColumn.START_DATE)
            ),
            DatabaseColumn.END_DATE.value: parse_gtfs_date(
                gtfs_field(row, GtfsColumn.END_DATE)
            ),
        }

    def _map_trip(self, row: dict[str, str]) -> dict[str, Any]:
        return {
            DatabaseColumn.ROUTE_ID.value: clean(gtfs_field(row, GtfsColumn.ROUTE_ID)),
            DatabaseColumn.SERVICE_ID.value: clean(gtfs_field(row, GtfsColumn.SERVICE_ID)),
            DatabaseColumn.TRIP_ID.value: clean(gtfs_field(row, GtfsColumn.TRIP_ID)),
            DatabaseColumn.TRIP_HEADSIGN.value: clean(
                gtfs_field(row, GtfsColumn.TRIP_HEADSIGN)
            ),
            DatabaseColumn.DIRECTION_ID.value: parse_int(
                gtfs_field(row, GtfsColumn.DIRECTION_ID)
            ),
        }

    def _map_stop_time(self, row: dict[str, str]) -> dict[str, Any]:
        arrival_time = clean(gtfs_field(row, GtfsColumn.ARRIVAL_TIME))
        departure_time = clean(gtfs_field(row, GtfsColumn.DEPARTURE_TIME))
        return {
            DatabaseColumn.TRIP_ID.value: clean(gtfs_field(row, GtfsColumn.TRIP_ID)),
            DatabaseColumn.ARRIVAL_TIME.value: arrival_time,
            DatabaseColumn.DEPARTURE_TIME.value: departure_time,
            DatabaseColumn.ARRIVAL_SECONDS.value: parse_gtfs_time_to_seconds(arrival_time),
            DatabaseColumn.DEPARTURE_SECONDS.value: parse_gtfs_time_to_seconds(departure_time),
            DatabaseColumn.STOP_ID.value: clean(gtfs_field(row, GtfsColumn.STOP_ID)),
            DatabaseColumn.STOP_SEQUENCE.value: parse_int(
                gtfs_field(row, GtfsColumn.STOP_SEQUENCE)
            )
            or 0,
        }


def gtfs_field(row: dict[str, str], column: GtfsColumn) -> str | None:
    return row.get(column.value)


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
    return clean(value) == GtfsValue.TRUE.value

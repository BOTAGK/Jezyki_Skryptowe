from __future__ import annotations

from sqlalchemy import Integer, cast, func, select
from sqlalchemy.orm import Session

from timetable.constants import AnalyticsDefault, AnalyticsLabel
from timetable.models import Route, StopTime, Trip
from timetable.schemas.analytics import DirectionStatistic, HourlyStatistic
from timetable.utils.time import format_gtfs_seconds


class AnalyticsRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def count_distinct_routes(self, stop_id: str) -> int:
        statement = (
            select(func.count(func.distinct(Trip.route_id)))
            .select_from(StopTime)
            .join(Trip, Trip.trip_id == StopTime.trip_id)
            .where(StopTime.stop_id == stop_id)
        )
        return int(self.session.execute(statement).scalar_one() or 0)

    def count_departures(self, stop_id: str) -> int:
        statement = select(func.count(StopTime.id)).where(StopTime.stop_id == stop_id)
        return int(self.session.execute(statement).scalar_one() or 0)

    def departure_range(self, stop_id: str) -> tuple[str | None, str | None]:
        statement = select(
            func.min(StopTime.departure_seconds),
            func.max(StopTime.departure_seconds),
        ).where(StopTime.stop_id == stop_id)
        first_seconds, last_seconds = self.session.execute(statement).one()
        return format_gtfs_seconds(first_seconds), format_gtfs_seconds(last_seconds)

    def popular_directions(self, stop_id: str, limit: int = 5) -> list[DirectionStatistic]:
        direction_label = AnalyticsLabel.DIRECTION.value
        departures_label = AnalyticsLabel.DEPARTURES.value
        direction = func.coalesce(
            Trip.trip_headsign,
            AnalyticsDefault.UNKNOWN_DIRECTION.value,
        ).label(direction_label)
        departures = func.count(StopTime.id).label(departures_label)
        statement = (
            select(direction, departures)
            .select_from(StopTime)
            .join(Trip, Trip.trip_id == StopTime.trip_id)
            .where(StopTime.stop_id == stop_id)
            .group_by(direction)
            .order_by(departures.desc(), direction)
            .limit(limit)
        )
        return [
            DirectionStatistic(
                direction=str(row._mapping[direction_label]),
                departures=int(row._mapping[departures_label]),
            )
            for row in self.session.execute(statement)
        ]

    def busiest_hours(self, stop_id: str, limit: int = 6) -> list[HourlyStatistic]:
        hour_label = AnalyticsLabel.HOUR.value
        departures_label = AnalyticsLabel.DEPARTURES.value
        distinct_routes_label = AnalyticsLabel.DISTINCT_ROUTES.value
        hour = cast(StopTime.departure_seconds / 3600, Integer).label(hour_label)
        departures = func.count(StopTime.id).label(departures_label)
        distinct_routes = func.count(func.distinct(Route.route_id)).label(
            distinct_routes_label
        )

        statement = (
            select(hour, departures, distinct_routes)
            .select_from(StopTime)
            .join(Trip, Trip.trip_id == StopTime.trip_id)
            .join(Route, Route.route_id == Trip.route_id)
            .where(StopTime.stop_id == stop_id)
            .where(StopTime.departure_seconds.is_not(None))
            .group_by(hour)
            .order_by(departures.desc(), hour)
            .limit(limit)
        )

        return [
            HourlyStatistic(
                hour=int(row._mapping[hour_label]),
                departures=int(row._mapping[departures_label]),
                distinct_routes=int(row._mapping[distinct_routes_label]),
            )
            for row in self.session.execute(statement)
        ]

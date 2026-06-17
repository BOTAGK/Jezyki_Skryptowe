from __future__ import annotations

from sqlalchemy.orm import Session

from timetable.repositories.analytics_repository import AnalyticsRepository
from timetable.repositories.stop_repository import StopRepository
from timetable.schemas.analytics import StopAnalytics, StopOption


class AnalyticsService:
    def __init__(self, session: Session) -> None:
        self.stops = StopRepository(session)
        self.analytics = AnalyticsRepository(session)

    def list_stops(self, search: str | None = None, limit: int | None = None) -> list[StopOption]:
        return self.stops.list_stops(search=search, limit=limit)

    def analyze_stop(self, stop_id: str) -> StopAnalytics:
        stop = self.stops.get(stop_id)
        if stop is None:
            raise LookupError(f"Stop not found: {stop_id}")

        first_departure, last_departure = self.analytics.departure_range(stop_id)
        return StopAnalytics(
            stop=StopOption(
                stop_id=stop.stop_id,
                stop_name=stop.stop_name,
                stop_code=stop.stop_code,
            ),
            route_count=self.analytics.count_distinct_routes(stop_id),
            departure_count=self.analytics.count_departures(stop_id),
            first_departure=first_departure,
            last_departure=last_departure,
            popular_directions=self.analytics.popular_directions(stop_id),
            busiest_hours=self.analytics.busiest_hours(stop_id),
        )

from __future__ import annotations

from dataclasses import dataclass

from timetable.constants import TimeToken


@dataclass(frozen=True, slots=True)
class StopOption:
    stop_id: str
    stop_name: str
    stop_code: str | None


@dataclass(frozen=True, slots=True)
class DirectionStatistic:
    direction: str
    departures: int


@dataclass(frozen=True, slots=True)
class HourlyStatistic:
    hour: int
    departures: int
    distinct_routes: int

    @property
    def hour_label(self) -> str:
        separator = TimeToken.SEPARATOR.value
        return f"{self.hour:02d}{separator}00-{self.hour:02d}{separator}59"


@dataclass(frozen=True, slots=True)
class StopAnalytics:
    stop: StopOption
    route_count: int
    departure_count: int
    first_departure: str | None
    last_departure: str | None
    popular_directions: list[DirectionStatistic]
    busiest_hours: list[HourlyStatistic]

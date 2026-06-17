from __future__ import annotations

from dataclasses import dataclass

from timetable.constants import TableName


@dataclass(slots=True)
class ImportSummary:
    stops: int = 0
    routes: int = 0
    service_calendar: int = 0
    trips: int = 0
    stop_times: int = 0

    def as_lines(self) -> list[str]:
        return [
            f"{TableName.STOPS.value}: {self.stops}",
            f"{TableName.ROUTES.value}: {self.routes}",
            f"{TableName.SERVICE_CALENDAR.value}: {self.service_calendar}",
            f"{TableName.TRIPS.value}: {self.trips}",
            f"{TableName.STOP_TIMES.value}: {self.stop_times}",
        ]

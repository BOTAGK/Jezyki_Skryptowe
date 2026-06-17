from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ImportSummary:
    stops: int = 0
    routes: int = 0
    service_calendar: int = 0
    trips: int = 0
    stop_times: int = 0

    def as_lines(self) -> list[str]:
        return [
            f"stops: {self.stops}",
            f"routes: {self.routes}",
            f"service_calendar: {self.service_calendar}",
            f"trips: {self.trips}",
            f"stop_times: {self.stop_times}",
        ]

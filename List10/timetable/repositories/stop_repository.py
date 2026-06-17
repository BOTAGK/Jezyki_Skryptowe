from __future__ import annotations

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from timetable.models import Stop
from timetable.schemas.analytics import StopOption


class StopRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get(self, stop_id: str) -> Stop | None:
        return self.session.get(Stop, stop_id)

    def list_stops(self, search: str | None = None, limit: int | None = None) -> list[StopOption]:
        statement: Select[tuple[Stop]] = select(Stop).order_by(Stop.stop_name, Stop.stop_id)

        if search:
            pattern = f"%{search}%"
            statement = statement.where(Stop.stop_name.ilike(pattern))

        if limit is not None:
            statement = statement.limit(limit)

        stops = self.session.execute(statement).scalars().all()
        return [
            StopOption(
                stop_id=stop.stop_id,
                stop_name=stop.stop_name,
                stop_code=stop.stop_code,
            )
            for stop in stops
        ]

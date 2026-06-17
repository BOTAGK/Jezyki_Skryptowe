from __future__ import annotations

from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from timetable.constants import RelationshipName, TableName
from timetable.models.base import Base


class Stop(Base):
    __tablename__ = TableName.STOPS.value

    stop_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    stop_code: Mapped[str | None] = mapped_column(String(64))
    stop_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    stop_lat: Mapped[float | None] = mapped_column(Float)
    stop_lon: Mapped[float | None] = mapped_column(Float)

    stop_times: Mapped[list["StopTime"]] = relationship(
        back_populates=RelationshipName.STOP.value
    )

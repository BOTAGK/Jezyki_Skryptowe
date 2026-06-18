from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from timetable.constants import (
    ConstraintName,
    DatabaseColumn,
    ForeignKeyAction,
    IndexName,
    RelationshipName,
    TableName,
    foreign_key_target,
)
from timetable.models.base import Base

if TYPE_CHECKING:
    from timetable.models.trip import Trip
    from timetable.models.stop import Stop
class StopTime(Base):
    __tablename__ = TableName.STOP_TIMES.value
    __table_args__ = (
        UniqueConstraint(
            DatabaseColumn.TRIP_ID.value,
            DatabaseColumn.STOP_SEQUENCE.value,
            name=ConstraintName.STOP_TIMES_TRIP_SEQUENCE.value,
        ),
        Index(
            IndexName.STOP_TIMES_STOP_DEPARTURE.value,
            DatabaseColumn.STOP_ID.value,
            DatabaseColumn.DEPARTURE_SECONDS.value,
        ),
        Index(
            IndexName.STOP_TIMES_TRIP_SEQUENCE.value,
            DatabaseColumn.TRIP_ID.value,
            DatabaseColumn.STOP_SEQUENCE.value,
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    trip_id: Mapped[str] = mapped_column(
        String(128),
        ForeignKey(
            foreign_key_target(TableName.TRIPS, DatabaseColumn.TRIP_ID),
            ondelete=ForeignKeyAction.CASCADE.value,
            onupdate=ForeignKeyAction.CASCADE.value,
        ),
        nullable=False,
    )
    arrival_time: Mapped[str | None] = mapped_column(String(16))
    departure_time: Mapped[str | None] = mapped_column(String(16))
    arrival_seconds: Mapped[int | None] = mapped_column(Integer)
    departure_seconds: Mapped[int | None] = mapped_column(Integer)
    stop_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey(
            foreign_key_target(TableName.STOPS, DatabaseColumn.STOP_ID),
            ondelete=ForeignKeyAction.RESTRICT.value,
            onupdate=ForeignKeyAction.CASCADE.value,
        ),
        nullable=False,
    )
    stop_sequence: Mapped[int] = mapped_column(Integer, nullable=False)

    trip: Mapped["Trip"] = relationship(back_populates=RelationshipName.STOP_TIMES.value)
    stop: Mapped["Stop"] = relationship(back_populates=RelationshipName.STOP_TIMES.value)

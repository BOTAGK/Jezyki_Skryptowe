from __future__ import annotations

from sqlalchemy import ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from timetable.models.base import Base


class StopTime(Base):
    __tablename__ = "stop_times"
    __table_args__ = (
        UniqueConstraint("trip_id", "stop_sequence", name="uq_stop_times_trip_sequence"),
        Index("ix_stop_times_stop_departure", "stop_id", "departure_seconds"),
        Index("ix_stop_times_trip_sequence", "trip_id", "stop_sequence"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    trip_id: Mapped[str] = mapped_column(
        String(128),
        ForeignKey("trips.trip_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    arrival_time: Mapped[str | None] = mapped_column(String(16))
    departure_time: Mapped[str | None] = mapped_column(String(16))
    arrival_seconds: Mapped[int | None] = mapped_column(Integer)
    departure_seconds: Mapped[int | None] = mapped_column(Integer)
    stop_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("stops.stop_id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    stop_sequence: Mapped[int] = mapped_column(Integer, nullable=False)

    trip: Mapped["Trip"] = relationship(back_populates="stop_times")
    stop: Mapped["Stop"] = relationship(back_populates="stop_times")

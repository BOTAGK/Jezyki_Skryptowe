from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from timetable.models.base import Base


class Trip(Base):
    __tablename__ = "trips"

    trip_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    route_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("routes.route_id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    service_id: Mapped[str | None] = mapped_column(
        String(64),
        ForeignKey("service_calendar.service_id", ondelete="RESTRICT", onupdate="CASCADE"),
        index=True,
    )
    trip_headsign: Mapped[str | None] = mapped_column(String(255))
    direction_id: Mapped[int | None] = mapped_column(Integer)

    route: Mapped["Route"] = relationship(back_populates="trips")
    calendar: Mapped["ServiceCalendar | None"] = relationship(back_populates="trips")
    stop_times: Mapped[list["StopTime"]] = relationship(
        back_populates="trip",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from timetable.constants import (
    CascadeOption,
    DatabaseColumn,
    ForeignKeyAction,
    RelationshipName,
    TableName,
    foreign_key_target,
)
from timetable.models.base import Base

if TYPE_CHECKING:
    from timetable.models.route import Route
    from timetable.models.calendar import ServiceCalendar
    from timetable.models.stop_time import StopTime


class Trip(Base):
    __tablename__ = TableName.TRIPS.value

    trip_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    route_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey(
            foreign_key_target(TableName.ROUTES, DatabaseColumn.ROUTE_ID),
            ondelete=ForeignKeyAction.RESTRICT.value,
            onupdate=ForeignKeyAction.CASCADE.value,
        ),
        nullable=False,
        index=True,
    )
    service_id: Mapped[str | None] = mapped_column(
        String(64),
        ForeignKey(
            foreign_key_target(TableName.SERVICE_CALENDAR, DatabaseColumn.SERVICE_ID),
            ondelete=ForeignKeyAction.RESTRICT.value,
            onupdate=ForeignKeyAction.CASCADE.value,
        ),
        index=True,
    )
    trip_headsign: Mapped[str | None] = mapped_column(String(255))
    direction_id: Mapped[int | None] = mapped_column(Integer)

    route: Mapped["Route"] = relationship(back_populates=RelationshipName.TRIPS.value)
    calendar: Mapped["ServiceCalendar | None"] = relationship(
        back_populates=RelationshipName.TRIPS.value
    )
    stop_times: Mapped[list["StopTime"]] = relationship(
        back_populates=RelationshipName.TRIP.value,
        cascade=CascadeOption.ALL_DELETE_ORPHAN.value,
        passive_deletes=True,
    )

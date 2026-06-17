from __future__ import annotations

from datetime import date

from sqlalchemy import Boolean, Date, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from timetable.constants import RelationshipName, TableName
from timetable.models.base import Base


class ServiceCalendar(Base):
    __tablename__ = TableName.SERVICE_CALENDAR.value

    service_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    monday: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    tuesday: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    wednesday: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    thursday: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    friday: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    saturday: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    sunday: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    start_date: Mapped[date | None] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date)

    trips: Mapped[list["Trip"]] = relationship(
        back_populates=RelationshipName.CALENDAR.value
    )

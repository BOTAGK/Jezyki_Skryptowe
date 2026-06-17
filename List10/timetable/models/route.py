from __future__ import annotations

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from timetable.models.base import Base


class Route(Base):
    __tablename__ = "routes"

    route_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    agency_id: Mapped[str | None] = mapped_column(String(64))
    route_short_name: Mapped[str | None] = mapped_column(String(64))
    route_long_name: Mapped[str | None] = mapped_column(String(255))
    route_desc: Mapped[str | None] = mapped_column(Text)
    route_type: Mapped[int | None] = mapped_column(Integer)

    trips: Mapped[list["Trip"]] = relationship(back_populates="route")

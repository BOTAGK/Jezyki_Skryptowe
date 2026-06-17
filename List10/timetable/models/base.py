from __future__ import annotations

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from timetable.constants import NamingConventionKey, NamingConventionPattern


NAMING_CONVENTION = {
    NamingConventionKey.INDEX.value: NamingConventionPattern.INDEX.value,
    NamingConventionKey.UNIQUE.value: NamingConventionPattern.UNIQUE.value,
    NamingConventionKey.CHECK.value: NamingConventionPattern.CHECK.value,
    NamingConventionKey.FOREIGN_KEY.value: NamingConventionPattern.FOREIGN_KEY.value,
    NamingConventionKey.PRIMARY_KEY.value: NamingConventionPattern.PRIMARY_KEY.value,
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)

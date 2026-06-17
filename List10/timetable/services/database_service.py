from __future__ import annotations

from contextlib import AbstractContextManager
from pathlib import Path

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from timetable.database import (
    create_session_factory,
    create_sqlite_engine,
    normalize_database_path,
    session_scope,
)
from timetable.models import Base


class DatabaseService:
    def __init__(self, database: str | Path, echo: bool = False) -> None:
        self.database_path = normalize_database_path(database)
        self.engine: Engine = create_sqlite_engine(self.database_path, echo=echo)
        self.session_factory: sessionmaker[Session] = create_session_factory(self.engine)

    def create_schema(self, drop_existing: bool = False) -> None:
        if drop_existing:
            Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    def session(self) -> AbstractContextManager[Session]:
        return session_scope(self.session_factory)

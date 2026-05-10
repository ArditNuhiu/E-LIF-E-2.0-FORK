from __future__ import annotations

import logging
from typing import List, Optional

from sqlalchemy.engine import Engine
from sqlmodel import Session, select

from ..domain.models import DailyEntry, User

logger = logging.getLogger(__name__)


class BaseDAO:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def session(self) -> Session:
        return Session(self.engine)


class EntryDAO(BaseDAO):

    def create(self, entry: DailyEntry) -> DailyEntry:
        logger.debug("Creating entry for user_id: %s, date: %s", entry.user_id, entry.date)
        with self.session() as session:
            session.add(entry)
            session.commit()
            session.refresh(entry)
            logger.debug("Entry created with id: %s, score: %s", entry.id, entry.score)
            return entry

    def list_all(self) -> List[DailyEntry]:
        with self.session() as session:
            return list(session.exec(select(DailyEntry)).all())

    def get_by_id(self, entry_id: int) -> Optional[DailyEntry]:
        with self.session() as session:
            return session.get(DailyEntry, entry_id)


class UserDAO(BaseDAO):

    def create(self, user: User) -> User:
        with self.session() as session:
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    def get_by_username(self, username: str) -> Optional[User]:
        logger.debug("Looking up user: %s", username)
        with self.session() as session:
            user = session.exec(select(User).where(User.username == username)).first()
            if user:
                logger.debug("User '%s' found", username)
            else:
                logger.debug("User '%s' not found", username)
            return user
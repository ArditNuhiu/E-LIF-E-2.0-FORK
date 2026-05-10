from __future__ import annotations

import logging
from typing import Optional

from nicegui import ui

from .data_access.db import Database
from .data_access.dao import EntryDAO, UserDAO
from .domain.models import User
from .logging_config import setup_logging
from .services.wellness_service import WellnessService
from .ui.Login import create_login_page
from .ui.Dashboard import create_dashboard_page

logger = logging.getLogger(__name__)


class ElifeApplication:
    """Application composition root."""

    def __init__(self, database: Optional[Database] = None) -> None:
        setup_logging()
        logger.debug("ElifeApplication initialising")

        self.database = database or Database()
        self.database.init_schema()
        logger.debug("Database schema initialised")

        engine = self.database.engine

        self.entry_dao = EntryDAO(engine)
        self.user_dao = UserDAO(engine)
        self.wellness_service = WellnessService()

        self._seed_default_user()

        create_login_page(self.user_dao)
        create_dashboard_page(self.entry_dao, self.wellness_service)
        logger.debug("Routes registered: / and /dashboard")

    def _seed_default_user(self) -> None:
        """Create a default admin user if no users exist."""
        if not self.user_dao.get_by_username('admin'):
            self.user_dao.create(User(username='admin', password='1234', gender='male'))
            logger.debug("Default admin user seeded")
        else:
            logger.debug("Default admin user already exists, skipping seed")

    def run(self, host: str = "0.0.0.0", port: int = 8080, reload: bool = False) -> None:
        logger.debug("Starting NiceGUI server on %s:%d", host, port)
        ui.run(host=host, port=port, reload=reload, storage_secret="elife_secret")

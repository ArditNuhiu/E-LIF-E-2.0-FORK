from __future__ import annotations
from sqlmodel import Session
from elife_app.domain.models import DailyEntry
from datetime import date, timedelta


class WellnessSeeder:
    """Seeds the database with sample wellness tracking data."""

    def seed(self, session: Session, days: int = 7) -> None:
        today = date.today()
        entries = []

        for i in range(days):
            entry = DailyEntry(
                date=today - timedelta(days=i),
                sleep_quality=(i % 11),
                stress=(i % 11),
                friends=i % 2,
                water_intake=float(i % 6),
                exercise=i % 2,
                mood=(i % 11),
                work_hours=float(i % 9),
                hobbies=i % 2,
                steps=(i % 10001) * 5,
                meds=i % 2,
                period=i % 2,
            )
            entries.append(entry)

        for entry in entries:
            session.add(entry)
        session.commit()

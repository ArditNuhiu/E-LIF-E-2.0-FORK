from datetime import date
from elife_app.data_access.dao import EntryDAO, UserDAO
from elife_app.domain.models import DailyEntry, User
from elife_app.services.wellness_service import WellnessService


def test_entry_is_linked_to_user(database):
    """Saved entry carries the correct user_id."""
    user_dao = UserDAO(database.engine)
    entry_dao = EntryDAO(database.engine)

    user = user_dao.create(User(username='alice', password='pass', gender='female'))

    entry = DailyEntry(
        date=date(2025, 3, 1),
        user_id=user.id,
        sleep_quality=7, stress=3, friends=1,
        water_intake=2.5, exercise=1, mood=7,
        work_hours=8.0, hobbies=1, steps=8000,
        meds=1, period=0,
    )
    saved = entry_dao.create(entry)

    assert saved.user_id == user.id


def test_high_stress_reduces_saved_score(database):
    """Score stored in DB reflects stress deduction."""
    entry_dao = EntryDAO(database.engine)
    service = WellnessService()

    base = dict(
        date=date(2025, 3, 2),
        sleep_quality=7, friends=1, water_intake=2.5,
        exercise=1, mood=7, work_hours=8.0,
        hobbies=1, steps=8000, meds=1, period=0,
    )

    low = DailyEntry(**base, stress=0)
    high = DailyEntry(**base, stress=10)

    service.calculate_score(low)
    service.calculate_score(high)

    saved_low = entry_dao.create(low)
    saved_high = entry_dao.create(high)

    assert saved_low.score > saved_high.score

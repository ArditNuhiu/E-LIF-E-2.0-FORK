# E-LIF-E 2.0 — Daily Wellness Tracker

A browser-based daily wellness tracker built with NiceGUI. Users log health data each day, receive a calculated wellness score (0–75), and get personalised advice.

---

## Python Version

**Python 3.11.x is required.** SQLModel has a known incompatibility with Python 3.12+.

To check:
```bash
python --version
```

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Running the App

```bash
python main.py
```

Opens at [http://localhost:8080](http://localhost:8080).

Default login: `admin` / `1234`

---

## Running Tests

```bash
# All tests
pytest

# Specific test file
pytest -v elife_app/tests/test_unit.py
pytest -v elife_app/tests/test_db.py
pytest -v elife_app/tests/test_integration.py
```

---

## Architecture

The app uses a layered MVC structure. `ElifeApplication` (`elife_app/application.py`) is the composition root — it wires together the database, DAOs, services, and NiceGUI routes at startup.

**Layer flow:** UI pages → DAO (data access) → Database (SQLite)

### Key Files

| File | Role |
|---|---|
| `main.py` | Entry point — creates `ElifeApplication` and calls `run()` |
| `elife_app/application.py` | Composition root; wires all dependencies and registers NiceGUI routes |
| `elife_app/domain/models.py` | SQLModel ORM models: `User`, `DailyEntry` |
| `elife_app/data_access/db.py` | `Database` class: engine creation, schema init, session scope |
| `elife_app/data_access/dao.py` | `EntryDAO`, `UserDAO` — data access layer |
| `elife_app/services/wellness_service.py` | Score calculation and weekly report logic |
| `elife_app/ui/Login.py` | NiceGUI login page (route `/`) |
| `elife_app/ui/Dashboard.py` | NiceGUI daily check-in page (route `/dashboard`) |

### Wellness Score

The score is calculated from:

| Factor | Points |
|---|---|
| Sleep quality | 0–10 |
| Mood | 0–10 |
| Friends (saw friends today) | 0 or 10 |
| Exercise | 0 or 10 |
| Hobbies | 0 or 10 |
| Medication taken | 0 or 10 |
| Steps (1 pt per 5000, max 10) | 0–10 |
| Water intake (1 pt per litre, max 5) | 0–5 |
| Stress level (deducted) | −0 to −10 |
| Excess work hours over 8 (deducted) | −0 to −8 |

**Maximum score: 75**

---

## Database

- Default: `sqlite:///data/elife.db` (created automatically on first run)
- Override via `DATABASE_URL` environment variable
- Tests use `sqlite:///:memory:`

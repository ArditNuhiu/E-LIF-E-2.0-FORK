# Refactoring Change Log

Documents every change made during the E-LIF-E 2.0 refactor, which file was affected, and why.

---

## 1. Deleted Legacy CLI Code

**Files removed:**
- `elife_app/main.py`
- `elife_app/01 Previous Project/` (entire folder)

**Why:** The app was rewritten as a NiceGUI web app. The old terminal-based CLI used broken imports (`WellnessDAO`, `create_db`) that no longer exist and could not run. Keeping it caused confusion about which `main.py` was the real entry point.

---

## 2. Fixed Score Formula

**File:** `elife_app/services/wellness_service.py`

**What changed:** `stress` and `work_hours` are now factored into the score:
- `stress` is subtracted directly (range 0–10)
- Work hours over 8 are subtracted (e.g. 12 hours → −4)
- Score is clamped to `max(0, score)` to prevent negative values

**Why:** Both values were collected from the user and stored in the database but had no effect on the score. A user with maximum stress and 16-hour work days would receive the same score as someone relaxed and working normal hours — making the score misleading.

Also removed a dead `sys.path.insert` call that appeared after the import it was meant to enable, making it a no-op.

---

## 3. Added user_id to DailyEntry

**File:** `elife_app/domain/models.py`

**What changed:** Added `user_id: Optional[int] = Field(default=None, foreign_key="user.id")` to `DailyEntry`.

**Why:** Without this field, entries belonged to nobody. The weekly report mixed data from all users together and there was no way to query "entries for this user".

> Note: If you have an existing `data/elife.db`, delete it before running — SQLite does not auto-add columns to existing tables.

---

## 4. Fixed WellnessSeeder

**File:** `elife_app/data_access/seed.py`

**What changed:**
- Added `session.commit()` at the end of `seed()`
- Removed dead `sys.path.insert` call

**Why:** Without `commit()`, seeded data was silently discarded unless the caller manually committed. The `sys.path.insert` appeared after the import it was meant to enable and had no effect.

---

## 5. Wired Login to Real Database

**Files:** `elife_app/ui/Login.py`, `elife_app/application.py`

**What changed:**
- Fixed `Can from nicegui import ui, app` syntax error on line 1 of `Login.py`
- `create_login_page()` now accepts a `UserDAO` parameter
- Login checks the database instead of comparing against hardcoded `admin`/`1234`
- On success, stores both `username` and `user_id` in session storage
- `ElifeApplication` seeds a default `admin`/`1234` user on first run if no users exist

**Why:** Hardcoded credentials mean only one user can ever log in. `UserDAO` and the `User` model already existed but were never connected to the login flow.

---

## 6. Added Period Pain and Flow UI Fields

**File:** `elife_app/ui/Dashboard.py`

**What changed:**
- Added `period_pain` slider (0–10) and `period_flow` slider (0–3) to the dashboard
- Both fields are hidden by default and appear only when the period checkbox is checked
- Values are passed to `DailyEntry` on submit (or `None` if period is unchecked)
- `user_id` is now passed to `DailyEntry` from session storage

**Why:** The database schema had `period_pain` and `period_flow` fields but there was no UI to enter them. Users on their period could not log pain or flow data.

---

## 7. Added Integration Tests

**File:** `elife_app/tests/test_integration.py`

**What changed:** Added two integration tests:
1. Verifies that a submitted entry is saved with the correct `user_id`
2. Verifies that a high-stress entry receives a lower score than a low-stress entry, and that the difference is persisted to the database

**Why:** The file existed but was empty. End-to-end flows were completely untested.

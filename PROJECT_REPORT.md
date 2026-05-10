Can# E-LIF-E 2.0 — Project Report

## Python Version

**Required: Python 3.11.x**

SQLModel has a known incompatibility with Python 3.12+. The project was developed and tested on **Python 3.11.14 / 3.11.15**. Do not upgrade beyond 3.11 until SQLModel officially supports newer versions.

To check your version:
```bash
python --version
```

---

## Errors Found

### 1. SyntaxError in `test_db.py` (line 11) — Critical

**File:** `elife_app/tests/test_db.py`

A line of `==` characters was used as a visual separator instead of a comment:

```python
# Wrong — crashes the entire file at import time
== == == == == == == == == == == == == == == ==

# Correct
# ============================================================================
```

**Impact:** All three tests inside `test_db.py` were completely unreachable. The test runner would exit with a collection error before running any test.

**Status:** Fixed.

---

### 2. `sys.path.insert` Placed After the Import It Is Meant to Enable

**Files:** `elife_app/services/wellness_service.py`, `elife_app/data_access/seed.py`

Both files insert the project root into `sys.path` to allow absolute imports — but they do so *after* already importing from `elife_app`:

```python
# wellness_service.py
from elife_app.domain.models import DailyEntry  # line 1 — import happens here
import sys
from pathlib import Path
sys.path.insert(0, ...)  # line 6 — too late, import already resolved above
```

**Impact:** The `sys.path.insert` is a no-op. If the package were not already importable (e.g., running from a different directory), the import on line 1 would fail before the path fix is ever reached.

**Fix:** Remove the `sys.path.insert` calls entirely. When running from the project root with `pytest` or `python main.py`, Python finds the package correctly without manual path manipulation.

---

### 3. `WellnessSeeder.seed()` Never Commits

**File:** `elife_app/data_access/seed.py`

The `seed()` method adds entries to the session but never calls `session.commit()`:

```python
def seed(self, session: Session, days: int = 7) -> None:
    for entry in entries:
        session.add(entry)
    # Missing: session.commit()
```

**Impact:** Any data seeded through this class is silently discarded unless the caller commits the session externally. This is a hidden dependency that makes the seeder unreliable.

**Fix:** Add `session.commit()` at the end of the method, or document clearly that the caller is responsible for committing.

---

### 4. Period Pain and Flow Have No UI Fields

**File:** `elife_app/ui/Dashboard.py`

The `DailyEntry` model has `period_pain` and `period_flow` fields. The dashboard has a `period` checkbox, but no inputs appear for pain or flow when the user checks it:

```python
period = ui.checkbox('Are you on your period?')
# period_pain and period_flow inputs are never created
```

**Impact:** Users on their period cannot log pain or flow data, even though the database is designed to store it.

**Fix:** Add conditional UI elements that appear when the period checkbox is checked, and include those values when constructing the `DailyEntry` object.

---

### 5. `stress` and `work_hours` Are Collected but Ignored in Scoring

**File:** `elife_app/services/wellness_service.py`

The score formula does not include `stress` or `work_hours`, even though both are collected from the user and stored:

```python
score = (
    entry.sleep_quality +
    entry.mood +
    entry.friends * 10 +
    entry.exercise * 10 +
    entry.hobbies * 10 +
    entry.meds * 10 +
    min(entry.steps // 5000, 10) +
    min(int(entry.water_intake), 10)
    # stress and work_hours are never used here
)
```

**Impact:** High stress or excessive work hours have no negative effect on the wellness score. This makes the score misleading.

**Fix:** Subtract from the score based on stress level and excess work hours. For example:

```python
score = (
    ...existing terms...
    - entry.stress          # high stress lowers score
    - max(0, int(entry.work_hours) - 8)  # penalise hours over 8
)
score = max(0, score)  # clamp to avoid negative scores
```

---

### 6. Two `main.py` Files — Confusing Entry Points

**Files:** `main.py` (root), `elife_app/main.py`

There are two files with the same name serving completely different purposes:

| File | Purpose |
|---|---|
| `main.py` (root) | Current entry point — starts the NiceGUI web app |
| `elife_app/main.py` | Old Phase 1 CLI — terminal-based interface, no longer functional |

`elife_app/main.py` references `WellnessDAO` and `create_db` which no longer exist. Running it would crash immediately.

**Fix:** Delete `elife_app/main.py` or move it to the `elife_app/01 Previous Project/` folder alongside the other legacy code.

---

### 7. Login Is Hardcoded

**File:** `elife_app/ui/Login.py`

Authentication is hardcoded:

```python
if username == 'admin' and password == '1234':
```

**Impact:** Only one user can ever log in. The `UserDAO` and `User` model exist and are ready to use, but they are not connected to the login flow.

**Fix:** Use `UserDAO.get_by_username()` to look up the user and verify the password:

```python
user = user_dao.get_by_username(username)
if user and user.password == password:
    app.storage.user['username'] = username
    ui.navigate.to('/dashboard')
```

> Note: For a school project, storing and comparing plain-text passwords is acceptable. In a real application, passwords must be hashed (e.g., using `bcrypt`).

---

### 8. `DailyEntry` Has No `user_id` — Entries Are Not Linked to Users

**File:** `elife_app/domain/models.py`

The `DailyEntry` table has no foreign key to `User`, so there is no way to know which user submitted which entry:

```python
class DailyEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: date
    sleep_quality: int
    # ... no user_id field
```

**Impact:** All entries belong to nobody. Querying "entries for this user" is impossible. The weekly report shows data from all users mixed together.

**Fix:** Add a `user_id` field to `DailyEntry` and filter queries by it:

```python
user_id: Optional[int] = Field(default=None, foreign_key="user.id")
```

---

### 9. SyntaxError in `Login.py` (line 1)

**File:** `elife_app/ui/Login.py`

A stray word was prepended to the import statement, making the file unparseable:

```python
# Wrong — SyntaxError, app will crash on startup
Can from nicegui import ui, app

# Correct
from nicegui import ui, app
```

**Impact:** The entire NiceGUI app fails to start. Python cannot import `Login.py`, so no routes are registered and the server crashes immediately.

**Fix:** Remove the `Can` prefix from line 1.

---

### 10. `test_integration.py` Is Empty

**File:** `elife_app/tests/test_integration.py`

The file exists but contains no tests. This is not a crash, but it means end-to-end flows (e.g., submit a check-in through the UI and verify it is saved to the database) are untested.

---

## Recommended Fix Order for a School Project

Work through issues in this order — each step builds on the previous one:

1. **Fix the `sys.path.insert` calls** — clean up `wellness_service.py` and `seed.py`. Low effort, no risk.
2. **Delete `elife_app/main.py`** — remove the dead legacy entry point to avoid confusion.
3. **Add `user_id` to `DailyEntry`** — this is a database schema change and affects everything downstream, so do it early.
4. **Wire login to `UserDAO`** — replace the hardcoded credentials with a real lookup. Requires step 3 to be done first so users can own their entries.
5. **Fix the score formula** — include `stress` and `work_hours`. Update the tests in `test_unit.py` to reflect the new expected ranges.
6. **Add period pain/flow UI** — show `period_pain` and `period_flow` inputs conditionally when the period checkbox is checked.
7. **Fix `WellnessSeeder.seed()`** — add `session.commit()`.
8. **Write integration tests** — fill in `test_integration.py` with at least one end-to-end test: create a user, submit an entry, verify the score is saved.

---

## Summary Table

| # | File | Severity | Status |
|---|---|---|---|
| 1 | `tests/test_db.py:11` | Critical — SyntaxError | Fixed |
| 2 | `wellness_service.py`, `seed.py` | Low — dead code | Open |
| 3 | `data_access/seed.py` | Medium — data loss | Open |
| 4 | `ui/Dashboard.py` | Medium — missing feature | Open |
| 5 | `services/wellness_service.py` | Medium — wrong logic | Open |
| 6 | `elife_app/main.py` | Low — dead file | Open |
| 7 | `ui/Login.py` | High — hardcoded auth | Open |
| 8 | `domain/models.py` | High — missing relation | Open |
| 9 | `ui/Login.py:1` | Critical — SyntaxError, app won't start | Open |
| 10 | `tests/test_integration.py` | Low — no coverage | Open |

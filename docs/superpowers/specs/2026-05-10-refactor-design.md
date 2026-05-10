# E-LIF-E 2.0 Refactor Design

**Date:** 2026-05-10  
**Scope:** Full code cleanup, logic fixes, legacy removal, and documentation

---

## 1. Files to Delete

| File | Reason |
|---|---|
| `elife_app/main.py` | Dead CLI entry point with broken imports — no longer the app entry point |
| `elife_app/01 Previous Project/` | Entire legacy folder — Phase 1 CLI implementation, superseded by NiceGUI app |

---

## 2. Code Fixes

### `elife_app/domain/models.py`
- Add `user_id: Optional[int] = Field(default=None, foreign_key="user.id")` to `DailyEntry`
- Links each daily entry to the user who submitted it

### `elife_app/services/wellness_service.py`
- Remove `sys.path.insert` (no-op, placed after the import it was meant to enable)
- Include `stress` and `work_hours` in score calculation:
  - Subtract `entry.stress` (high stress lowers score)
  - Subtract `max(0, int(entry.work_hours) - 8)` (penalise hours over 8)
  - Clamp final score: `score = max(0, score)`

### `elife_app/data_access/seed.py`
- Remove `sys.path.insert` (same reason as above)
- Add `session.commit()` at the end of `WellnessSeeder.seed()` so seeded data is persisted

### `elife_app/ui/Login.py`
- Fix `Can from nicegui import ui, app` syntax error on line 1
- Accept `UserDAO` as an injected parameter via `create_login_page(user_dao)`
- Replace hardcoded `admin/1234` check with `user_dao.get_by_username(username)` lookup
- On success, store `username` in `app.storage.user` and navigate to `/dashboard`
- On failure, notify the user

### `elife_app/ui/Dashboard.py`
- Show `period_pain` slider (0–10) and `period_flow` slider (0–3) conditionally when the period checkbox is checked
- Pass `user_id` (from `app.storage.user`) when constructing `DailyEntry`

### `elife_app/application.py`
- Instantiate `UserDAO` alongside `EntryDAO`
- Pass `user_dao` into `create_login_page(user_dao)`

---

## 3. Tests

### `elife_app/tests/test_unit.py`
- Update score range assertions in `test_service_score` and `test_edge_case_all_perfect` to account for stress and work_hours deductions

### `elife_app/tests/test_integration.py`
- **Test 1:** Create a `User`, submit a `DailyEntry` via `EntryDAO`, verify entry is saved with the correct `user_id`
- **Test 2:** Submit an entry with `stress=10` and `work_hours=12`, verify score is lower than an identical entry with `stress=0` and `work_hours=8`

---

## 4. Markdown Files

### `README.md`
- Project overview and purpose
- Python version requirement (3.11.x) and why
- Installation instructions (`pip install -r requirements.txt`)
- How to run the app (`python main.py`)
- How to run tests (`pytest`)
- Architecture overview (layers, key files)

### `REFACTORING.md`
- One section per fix, describing what changed, which file, and why
- Maps to issues originally documented in `PROJECT_REPORT.md`

---

## 5. Out of Scope

- Password hashing (plain-text comparison is acceptable for a school project)
- User registration page (not broken, not in scope)
- UI styling changes

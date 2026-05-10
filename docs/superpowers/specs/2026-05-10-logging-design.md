# E-LIF-E 2.0 Logging Design

**Date:** 2026-05-10
**Scope:** Add debug-style terminal + file logging for troubleshooting

---

## 1. Setup

**New file:** `elife_app/logging_config.py`

Configures the Python root logger once. Called from `ElifeApplication.__init__` before any other setup.

**Format (both handlers):**
```
%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(funcName)s | %(message)s
```

**Example output:**
```
2026-05-10 19:45:01 | DEBUG    | application.py:28 | _seed_default_user | Seeding default admin user
2026-05-10 19:45:02 | WARNING  | Login.py:22 | login | Failed login attempt for username: wronguser
```

**Handlers:**
- `StreamHandler` → terminal, level `DEBUG`
- `FileHandler` → `logs/elife.log`, level `DEBUG`, plain text
- `logs/` added to `.gitignore`

---

## 2. Events per File

### `elife_app/application.py`
- `DEBUG` — App starting on `{host}:{port}`
- `DEBUG` — Database schema initialised
- `DEBUG` — Default admin user seeded
- `DEBUG` — Default admin user already exists, skipping seed
- `DEBUG` — Routes registered

### `elife_app/ui/Login.py`
- `DEBUG` — Login attempt for username: `{username}`
- `DEBUG` — Login successful for username: `{username}`
- `WARNING` — Failed login attempt for username: `{username}`

### `elife_app/ui/Dashboard.py`
- `DEBUG` — Check-in submitted — user_id: `{user_id}`, date: `{date}`, score: `{score}`
- `DEBUG` — User `{username}` logged out

### `elife_app/data_access/dao.py`
- `DEBUG` — Creating entry for user_id: `{user_id}`, date: `{date}`
- `DEBUG` — Entry created with id: `{id}`, score: `{score}`
- `DEBUG` — Looking up user: `{username}`
- `DEBUG` — User `{username}` found / not found

---

## 3. Files Changed

| Action | File |
|---|---|
| Create | `elife_app/logging_config.py` |
| Modify | `elife_app/application.py` |
| Modify | `elife_app/ui/Login.py` |
| Modify | `elife_app/ui/Dashboard.py` |
| Modify | `elife_app/data_access/dao.py` |
| Modify | `.gitignore` |

---

## 4. Out of Scope

- Log rotation (not needed for a school project)
- Per-module log levels
- Logging inside `WellnessService` (pure calculation, no I/O)
- Logging inside `db.py` (SQLAlchemy's own `echo=True` covers DB-level SQL if needed)

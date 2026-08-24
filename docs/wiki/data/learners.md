# Table: learners

> **Sources** — interview Q6; `Proposal/Documentation/project_documentation.md:196-225,510-518`; `docs/sources/decisions/2026-08-24-learner-user-link.md`
> **Status** — [spec]
> **Page-size budget** — used 46 / 300 lines

<a id="purpose"></a>
## Purpose
One row per learner. `user_id` optionally links the learner to a `users` row of role `LEARNER` so the learner can log in.

<a id="schema"></a>
## Schema

```sql
-- backend/app/models/learner.py [planned]
CREATE TABLE learners (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id    INTEGER UNIQUE REFERENCES users(id),
  name       TEXT    NOT NULL,
  email      TEXT    NOT NULL UNIQUE,
  department TEXT    NOT NULL,
  status     TEXT    NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE','INACTIVE')),
  created_at TEXT    NOT NULL DEFAULT (datetime('now'))
);
```

<a id="columns"></a>
## Columns

| Column | Type | Nullable | Default | Constraint | Notes |
|---|---|---|---|---|---|
| id | INTEGER | no | autoincrement | PK | |
| user_id | INTEGER | yes | NULL | UNIQUE FK → users.id | links login account per [learner-user-link ADR](../../sources/decisions/2026-08-24-learner-user-link.md) |
| name | TEXT | no | — | — | required |
| email | TEXT | no | — | UNIQUE | required |
| department | TEXT | no | — | — | required |
| status | TEXT | no | `ACTIVE` | `ACTIVE` \| `INACTIVE` | |
| created_at | TEXT | no | `datetime('now')` | — | ISO-8601 UTC |

<a id="invariants"></a>
## Invariants
- `email` is unique.
- `user_id`, when set, references a `users` row of role `LEARNER` and is unique.

<a id="read-patterns"></a>
## Read patterns
- List → [api/learners/list-learners.md](../api/learners/list-learners.md)
- By `id` → [api/learners/get-learner.md](../api/learners/get-learner.md)

<a id="write-patterns"></a>
## Write patterns
- Insert → [api/learners/create-learner.md](../api/learners/create-learner.md)
- Update → [api/learners/update-learner.md](../api/learners/update-learner.md)
- Delete → [api/learners/delete-learner.md](../api/learners/delete-learner.md)

<a id="volume"></a>
## Volume estimates
- Demo scale: ~50 learners. Growth: negligible. Retention: indefinite (hard delete on demand).

<a id="verify"></a>
## Verify

```bash
python -c "import sqlite3; c=sqlite3.connect('backend/training_demo.db'); print([r[1] for r in c.execute('PRAGMA table_info(learners)')])"
```
Expected: `['id','user_id','name','email','department','status','created_at']`.

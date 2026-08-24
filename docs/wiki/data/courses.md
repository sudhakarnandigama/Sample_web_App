# Table: courses

> **Sources** — interview Q6; `Proposal/Documentation/project_documentation.md:165-193,496-506`; `docs/sources/decisions/2026-08-24-schema-concretizations.md`
> **Status** — [spec]
> **Page-size budget** — used 46 / 300 lines

<a id="purpose"></a>
## Purpose
One row per training course. Admin creates, edits, activates/deactivates, and deletes courses.

<a id="schema"></a>
## Schema

```sql
-- backend/app/models/course.py [planned]
CREATE TABLE courses (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  title          TEXT    NOT NULL,
  description    TEXT    NOT NULL,
  duration_hours INTEGER NOT NULL CHECK (duration_hours > 0),
  status         TEXT    NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE','INACTIVE')),
  created_at     TEXT    NOT NULL DEFAULT (datetime('now'))
);
```

<a id="columns"></a>
## Columns

| Column | Type | Nullable | Default | Constraint | Notes |
|---|---|---|---|---|---|
| id | INTEGER | no | autoincrement | PK | |
| title | TEXT | no | — | — | required |
| description | TEXT | no | — | — | required |
| duration_hours | INTEGER | no | — | `> 0` | PRD §6 `Duration`; unit = hours per [schema ADR](../../sources/decisions/2026-08-24-schema-concretizations.md) |
| status | TEXT | no | `ACTIVE` | `ACTIVE` \| `INACTIVE` | activate/deactivate (§6) |
| created_at | TEXT | no | `datetime('now')` | — | ISO-8601 UTC |

<a id="invariants"></a>
## Invariants
- `title` is non-empty.
- `duration_hours > 0`.
- `status` is `ACTIVE` or `INACTIVE`.

<a id="read-patterns"></a>
## Read patterns
- List → [api/courses/list-courses.md](../api/courses/list-courses.md)
- By `id` → [api/courses/get-course.md](../api/courses/get-course.md)

<a id="write-patterns"></a>
## Write patterns
- Insert → [api/courses/create-course.md](../api/courses/create-course.md)
- Update → [api/courses/update-course.md](../api/courses/update-course.md)
- Delete → [api/courses/delete-course.md](../api/courses/delete-course.md)

<a id="volume"></a>
## Volume estimates
- Demo scale: ~10 courses. Growth: negligible. Retention: indefinite (hard delete on demand).

<a id="verify"></a>
## Verify

```bash
python -c "import sqlite3; c=sqlite3.connect('backend/training_demo.db'); print([r[1] for r in c.execute('PRAGMA table_info(courses)')])"
```
Expected: `['id','title','description','duration_hours','status','created_at']`.

# Table: course_assignments

> **Sources** — interview Q6; `Proposal/Documentation/project_documentation.md:229-253,522-532`; `docs/sources/decisions/2026-08-24-schema-concretizations.md`
> **Status** — [spec]
> **Page-size budget** — used 46 / 300 lines

<a id="purpose"></a>
## Purpose
One row per course↔learner link. Tracks the learner's progress percentage and status on that course.

<a id="schema"></a>
## Schema

```sql
-- backend/app/models/assignment.py [planned]
CREATE TABLE course_assignments (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  course_id     INTEGER NOT NULL REFERENCES courses(id),
  learner_id    INTEGER NOT NULL REFERENCES learners(id),
  progress      INTEGER NOT NULL DEFAULT 0 CHECK (progress BETWEEN 0 AND 100),
  status        TEXT    NOT NULL DEFAULT 'NOT_STARTED' CHECK (status IN ('NOT_STARTED','IN_PROGRESS','COMPLETED')),
  assigned_date TEXT    NOT NULL DEFAULT (datetime('now')),
  UNIQUE (course_id, learner_id)
);
```

<a id="columns"></a>
## Columns

| Column | Type | Nullable | Default | Constraint | Notes |
|---|---|---|---|---|---|
| id | INTEGER | no | autoincrement | PK | |
| course_id | INTEGER | no | — | FK → courses.id | |
| learner_id | INTEGER | no | — | FK → learners.id | |
| progress | INTEGER | no | `0` | `0..100` | percentage |
| status | TEXT | no | `NOT_STARTED` | `NOT_STARTED` \| `IN_PROGRESS` \| `COMPLETED` | §8 states |
| assigned_date | TEXT | no | `datetime('now')` | — | ISO-8601 UTC |

<a id="invariants"></a>
## Invariants
- `(course_id, learner_id)` is unique — a learner is assigned a course at most once.
- `progress` is in `0..100`.
- `status` is `NOT_STARTED`, `IN_PROGRESS`, or `COMPLETED`.
- Setting `progress = 100` implies `status = COMPLETED`.

<a id="read-patterns"></a>
## Read patterns
- List by learner (learner dashboard) → [api/assignments/00-overview.md](../api/assignments/00-overview.md)
- List by course (admin report) → [ui/reports.md](../ui/reports.md)

<a id="write-patterns"></a>
## Write patterns
- Insert → [api/assignments/create-assignment.md](../api/assignments/create-assignment.md)
- Update progress/status → [api/assignments/update-progress.md](../api/assignments/update-progress.md)

<a id="volume"></a>
## Volume estimates
- Demo scale: ~10 courses × ~50 learners worst case. Growth: negligible.

<a id="verify"></a>
## Verify

```bash
python -c "import sqlite3; c=sqlite3.connect('backend/training_demo.db'); print([r[1] for r in c.execute('PRAGMA table_info(course_assignments)')])"
```
Expected: `['id','course_id','learner_id','progress','status','assigned_date']`.

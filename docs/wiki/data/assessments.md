# Table: assessments

> **Sources** — interview Q6; `Proposal/Documentation/project_documentation.md:277-306,535-543`; `docs/sources/decisions/2026-08-24-schema-concretizations.md`
> **Status** — [spec]
> **Page-size budget** — used 43 / 300 lines

<a id="purpose"></a>
## Purpose
One row per course assessment. A course has at most one assessment; the assessment holds `questions`.

<a id="schema"></a>
## Schema

```sql
-- backend/app/models/assessment.py [planned]
CREATE TABLE assessments (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  course_id     INTEGER NOT NULL REFERENCES courses(id),
  title         TEXT    NOT NULL,
  passing_score INTEGER NOT NULL DEFAULT 60 CHECK (passing_score BETWEEN 0 AND 100),
  UNIQUE (course_id)
);
```

<a id="columns"></a>
## Columns

| Column | Type | Nullable | Default | Constraint | Notes |
|---|---|---|---|---|---|
| id | INTEGER | no | autoincrement | PK | |
| course_id | INTEGER | no | — | UNIQUE FK → courses.id | one assessment per course |
| title | TEXT | no | — | — | |
| passing_score | INTEGER | no | `60` | `0..100` | pass threshold % per [schema ADR](../../sources/decisions/2026-08-24-schema-concretizations.md) |

<a id="invariants"></a>
## Invariants
- `course_id` is unique — one assessment per course.
- `passing_score` is in `0..100`. A score `>= passing_score` ⇒ `PASS`.

<a id="read-patterns"></a>
## Read patterns
- By `course_id` → [api/assessments/get-assessment.md](../api/assessments/get-assessment.md)

<a id="write-patterns"></a>
## Write patterns
- Seeded only. No create/update assessment endpoint exists in PRD §18–24. `[GAP-ASMT-01: assessment/question CRUD has no API — required before admin can manage assessments via UI]`

<a id="volume"></a>
## Volume estimates
- Demo scale: one per course (~10). Growth: negligible.

<a id="verify"></a>
## Verify

```bash
python -c "import sqlite3; c=sqlite3.connect('backend/training_demo.db'); print([r[1] for r in c.execute('PRAGMA table_info(assessments)')])"
```
Expected: `['id','course_id','title','passing_score']`.

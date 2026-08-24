# Table: assessment_attempts

> **Sources** — interview Q6; `Proposal/Documentation/project_documentation.md:277-306,561-570`; `docs/sources/decisions/2026-08-24-schema-concretizations.md`
> **Status** — [spec]
> **Page-size budget** — used 42 / 300 lines

<a id="purpose"></a>
## Purpose
One row per submitted assessment by a learner. Stores the computed score and pass/fail result.

<a id="schema"></a>
## Schema

```sql
-- backend/app/models/assessment.py [planned]
CREATE TABLE assessment_attempts (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  assessment_id INTEGER NOT NULL REFERENCES assessments(id),
  learner_id    INTEGER NOT NULL REFERENCES learners(id),
  score         INTEGER NOT NULL CHECK (score BETWEEN 0 AND 100),
  result        TEXT    NOT NULL CHECK (result IN ('PASS','FAIL')),
  attempted_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);
```

<a id="columns"></a>
## Columns

| Column | Type | Nullable | Default | Constraint | Notes |
|---|---|---|---|---|---|
| id | INTEGER | no | autoincrement | PK | |
| assessment_id | INTEGER | no | — | FK → assessments.id | |
| learner_id | INTEGER | no | — | FK → learners.id | |
| score | INTEGER | no | — | `0..100` | percentage correct |
| result | TEXT | no | — | `PASS` \| `FAIL` | score ≥ passing_score ⇒ PASS |
| attempted_at | TEXT | no | `datetime('now')` | — | ISO-8601 UTC |

<a id="invariants"></a>
## Invariants
- `result` is `PASS` iff `score >= assessments.passing_score` for the linked assessment.

<a id="read-patterns"></a>
## Read patterns
- List by learner → [ui/assessment-result.md](../ui/assessment-result.md)

<a id="write-patterns"></a>
## Write patterns
- Insert → [api/assessments/submit-assessment.md](../api/assessments/submit-assessment.md)

<a id="volume"></a>
## Volume estimates
- Demo scale: ≤ number of submissions. Growth: negligible.

<a id="verify"></a>
## Verify

```bash
python -c "import sqlite3; c=sqlite3.connect('backend/training_demo.db'); print([r[1] for r in c.execute('PRAGMA table_info(assessment_attempts)')])"
```
Expected: `['id','assessment_id','learner_id','score','result','attempted_at']`.

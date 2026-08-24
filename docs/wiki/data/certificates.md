# Table: certificates

> **Sources** — interview Q6; `Proposal/Documentation/project_documentation.md:309-338,574-583`; `docs/sources/decisions/2026-08-24-schema-concretizations.md`
> **Status** — [spec]
> **Page-size budget** — used 43 / 300 lines

<a id="purpose"></a>
## Purpose
One row per issued certificate. A certificate exists when a learner completed a course and passed its assessment.

<a id="schema"></a>
## Schema

```sql
-- backend/app/models/certificate.py [planned]
CREATE TABLE certificates (
  id                 INTEGER PRIMARY KEY AUTOINCREMENT,
  learner_id         INTEGER NOT NULL REFERENCES learners(id),
  course_id          INTEGER NOT NULL REFERENCES courses(id),
  certificate_number TEXT    NOT NULL UNIQUE,
  issued_date        TEXT    NOT NULL DEFAULT (datetime('now')),
  status             TEXT    NOT NULL DEFAULT 'CERTIFIED' CHECK (status IN ('CERTIFIED')),
  UNIQUE (learner_id, course_id)
);
```

<a id="columns"></a>
## Columns

| Column | Type | Nullable | Default | Constraint | Notes |
|---|---|---|---|---|---|
| id | INTEGER | no | autoincrement | PK | |
| learner_id | INTEGER | no | — | FK → learners.id | |
| course_id | INTEGER | no | — | FK → courses.id | |
| certificate_number | TEXT | no | — | UNIQUE | `CERT-{YYYY}-{3-digit seq}` per [schema ADR](../../sources/decisions/2026-08-24-schema-concretizations.md) |
| issued_date | TEXT | no | `datetime('now')` | — | ISO-8601 UTC |
| status | TEXT | no | `CERTIFIED` | `CERTIFIED` | |

<a id="invariants"></a>
## Invariants
- `certificate_number` is unique.
- `(learner_id, course_id)` is unique — one certificate per learner per course.
- A certificate is issued only when `course_assignments.status = COMPLETED` and the latest `assessment_attempts.result = PASS`.

<a id="read-patterns"></a>
## Read patterns
- List → [api/certificates/list-certificates.md](../api/certificates/list-certificates.md)
- By `id` → [api/certificates/get-certificate.md](../api/certificates/get-certificate.md)

<a id="write-patterns"></a>
## Write patterns
- Insert → [api/certificates/generate-certificate.md](../api/certificates/generate-certificate.md)

<a id="volume"></a>
## Volume estimates
- Demo scale: ≤ number of completed courses across learners. Growth: negligible.

<a id="verify"></a>
## Verify

```bash
python -c "import sqlite3; c=sqlite3.connect('backend/training_demo.db'); print([r[1] for r in c.execute('PRAGMA table_info(certificates)')])"
```
Expected: `['id','learner_id','course_id','certificate_number','issued_date','status']`.

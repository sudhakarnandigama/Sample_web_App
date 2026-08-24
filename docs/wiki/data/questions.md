# Table: questions

> **Sources** — interview Q6; `Proposal/Documentation/project_documentation.md:277-306,546-557`; `docs/sources/decisions/2026-08-24-schema-concretizations.md`
> **Status** — [spec]
> **Page-size budget** — used 43 / 300 lines

<a id="purpose"></a>
## Purpose
One row per multiple-choice question in an assessment. Four options, exactly one correct.

<a id="schema"></a>
## Schema

```sql
-- backend/app/models/assessment.py [planned]
CREATE TABLE questions (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  assessment_id INTEGER NOT NULL REFERENCES assessments(id),
  question_text TEXT    NOT NULL,
  option_a      TEXT    NOT NULL,
  option_b      TEXT    NOT NULL,
  option_c      TEXT    NOT NULL,
  option_d      TEXT    NOT NULL,
  correct_option TEXT   NOT NULL CHECK (correct_option IN ('A','B','C','D'))
);
```

<a id="columns"></a>
## Columns

| Column | Type | Nullable | Default | Constraint | Notes |
|---|---|---|---|---|---|
| id | INTEGER | no | autoincrement | PK | |
| assessment_id | INTEGER | no | — | FK → assessments.id | |
| question_text | TEXT | no | — | — | the prompt |
| option_a..option_d | TEXT | no | — | — | four answer options |
| correct_option | TEXT | no | — | `A` \| `B` \| `C` \| `D` | exactly one |

<a id="invariants"></a>
## Invariants
- `correct_option` is one of `A`, `B`, `C`, `D`.

<a id="read-patterns"></a>
## Read patterns
- By `assessment_id` (returned inside the assessment) → [api/assessments/get-assessment.md](../api/assessments/get-assessment.md)

<a id="write-patterns"></a>
## Write patterns
- Seeded only. `[GAP-ASMT-01: assessment/question CRUD has no API]`

<a id="volume"></a>
## Volume estimates
- Demo scale: ~10 questions per assessment (~100 total). Growth: negligible.

<a id="verify"></a>
## Verify

```bash
python -c "import sqlite3; c=sqlite3.connect('backend/training_demo.db'); print([r[1] for r in c.execute('PRAGMA table_info(questions)')])"
```
Expected: `['id','assessment_id','question_text','option_a','option_b','option_c','option_d','correct_option']`.

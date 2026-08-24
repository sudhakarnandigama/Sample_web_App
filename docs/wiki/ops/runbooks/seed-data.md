# Runbook: seed demo data

> **Sources** — `Proposal/Documentation/project_documentation.md:821-877`; [test/fixtures.md](../../test/fixtures.md)
> **Status** — [spec]
> **Page-size budget** — used 24 / 200 lines

<a id="when-to-use-this"></a>
## When to use this
After creating the DB, or whenever the demo data must be reset to the canonical set in [test/fixtures.md](../../test/fixtures.md).

<a id="pre-checks"></a>
## Pre-checks
- [ ] Backend venv active and deps installed (see [start-backend.md](start-backend.md)).

<a id="steps"></a>
## Steps
1. **Run seed script** — `python backend/seed.py` `[planned]` — expected: prints counts of inserted rows.
2. **Confirm login accounts** — `admin/admin123` and `learner/learner123` per [`project_documentation.md:821-838`](../../../../Proposal/Documentation/project_documentation.md:821).

<a id="verify"></a>
## Verify recovery

```bash
python -c "import sqlite3; c=sqlite3.connect('backend/training_demo.db'); print(c.execute('SELECT count(*) FROM users').fetchone()[0], c.execute('SELECT count(*) FROM courses').fetchone()[0])"
```
Expected: `2 3` (2 users, 3 courses).

<a id="rollback"></a>
## Rollback if step 1 fails
Delete `backend/training_demo.db`, fix the seed script, rerun step 1.

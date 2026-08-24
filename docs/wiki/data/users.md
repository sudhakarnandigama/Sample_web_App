# Table: users

> **Sources** — interview Q5, Q6; `Proposal/Documentation/project_documentation.md:477-493`; `docs/sources/decisions/2026-08-24-auth-transport.md`
> **Status** — [spec]
> **Page-size budget** — used 47 / 300 lines

<a id="purpose"></a>
## Purpose
One row per login account. The `role` column (`ADMIN` | `LEARNER`) drives authorization. Password is never stored in plaintext.

<a id="schema"></a>
## Schema

```sql
-- backend/app/models/user.py [planned]
CREATE TABLE users (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  username      TEXT    NOT NULL UNIQUE,
  password_hash TEXT    NOT NULL,
  role          TEXT    NOT NULL CHECK (role IN ('ADMIN','LEARNER')),
  full_name     TEXT    NOT NULL
);
```

<a id="columns"></a>
## Columns

| Column | Type | Nullable | Default | Constraint | Notes |
|---|---|---|---|---|---|
| id | INTEGER | no | autoincrement | PK | |
| username | TEXT | no | — | UNIQUE | login name |
| password_hash | TEXT | no | — | — | `pbkdf2_sha256$<salt>$<hash>` per [auth-transport ADR](../../sources/decisions/2026-08-24-auth-transport.md) |
| role | TEXT | no | — | `ADMIN` \| `LEARNER` | |
| full_name | TEXT | no | — | — | display name |

<a id="invariants"></a>
## Invariants
- `username` is unique.
- `password_hash` is a pbkdf2_sha256 hash — writing a plaintext password here is a bug.
- `role` is always `ADMIN` or `LEARNER`.

<a id="read-patterns"></a>
## Read patterns
- By `username` → [api/auth/login.md](../api/auth/login.md)

<a id="write-patterns"></a>
## Write patterns
- Insert via seed script only (no public create-user endpoint) → see [test/fixtures.md](../test/fixtures.md)

<a id="volume"></a>
## Volume estimates
- Demo scale: 2 seeded accounts (`admin`, `learner`) + as many learner accounts as learners created with logins.
- Growth: negligible. Retention: indefinite.

<a id="verify"></a>
## Verify

```bash
python -c "import sqlite3; c=sqlite3.connect('backend/training_demo.db'); print([r[1] for r in c.execute('PRAGMA table_info(users)')])"
```
Expected: `['id','username','password_hash','role','full_name']`.

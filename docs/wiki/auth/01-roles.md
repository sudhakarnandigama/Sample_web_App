# Role definitions

> **Sources** — interview Q5; `Proposal/Documentation/project_documentation.md:76-108`
> **Status** — [spec]
> **Page-size budget** — used 32 / 200 lines

Roles are the only two values of the JWT `role` claim. Scope assignment per role is canonical in [02-scopes.md](02-scopes.md).

| Role | JWT `role` value | Can do | Cannot do |
|---|---|---|---|
| Admin | `ADMIN` | login; manage courses, learners, assignments, assessments, certificates; view reports | act as a learner (no own-progress writes) |
| Learner | `LEARNER` | login; view assigned courses; update own progress; take assessments; view own results + certificates | manage courses/learners; view other learners' records |

<a id="admin"></a>
## Admin
Maps to `users.role = 'ADMIN'`. Capabilities listed in PRD §4.1. Holds every scope in [02-scopes.md](02-scopes.md) marked `admin`.

<a id="learner"></a>
## Learner
Maps to `users.role = 'LEARNER'` and (via `learners.user_id`) to one `learners` row. Capabilities listed in PRD §4.2. Holds every scope in [02-scopes.md](02-scopes.md) marked `learner`, scoped to own records only.

<a id="verify"></a>
## Verify

```bash
python -c "import sqlite3; c=sqlite3.connect('backend/training_demo.db'); print(sorted(r[0] for r in c.execute('SELECT DISTINCT role FROM users')))"
```
Expected: `['ADMIN','LEARNER']`.

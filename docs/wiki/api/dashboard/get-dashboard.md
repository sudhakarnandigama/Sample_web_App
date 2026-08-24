# GET /api/dashboard — dashboard summary

> **Sources** — interview Q2; `Proposal/Documentation/project_documentation.md:127-163,639-655`; [auth/02-scopes.md](../../auth/02-scopes.md#dashboard-read)
> **Status** — [spec]
> **Page-size budget** — used 52 / 300 lines

<a id="purpose"></a>
## Purpose
Returns summary counts for the dashboard. Fields differ by the caller's role.

<a id="auth"></a>
## Auth
- Required header: `Authorization: Bearer <jwt>`
- Required scope: `dashboard:read` — [auth/02-scopes.md#dashboard-read](../../auth/02-scopes.md#dashboard-read)
- Validation middleware: `backend/app/routers/dashboard.py` `[planned]`

<a id="request"></a>
## Request
No path, query, or body parameters.

<a id="responses"></a>
## Responses

### 200 OK — ADMIN
```json
{
  "total_learners": 5,
  "total_courses": 3,
  "active_courses": 2,
  "completed_courses": 2,
  "certificates": 2
}
```
PRD §19 example omits `active_courses`; §5.2 lists it, so both are included.

### 200 OK — LEARNER
```json
{
  "assigned_courses": 2,
  "in_progress": 1,
  "completed": 1,
  "certificates": 1
}
```

### 401 Unauthorized
`MISSING_AUTH` | `INVALID_TOKEN`

### 403 Forbidden
`INSUFFICIENT_SCOPE`

<a id="side-effects"></a>
## Side effects
None — read-only aggregate over [data/learners.md](../../data/learners.md), [data/courses.md](../../data/courses.md), [data/course_assignments.md](../../data/course_assignments.md), [data/certificates.md](../../data/certificates.md).

<a id="implementation"></a>
## Implementation
- Handler: `backend/app/routers/dashboard.py` `[planned]`

<a id="test-plan"></a>
## Test plan
| # | Case | Expected |
|---|---|---|
| 1 | ADMIN token | 200 with 5 admin fields |
| 2 | LEARNER token | 200 with 4 learner fields |
| 3 | no token | 401 `MISSING_AUTH` |

<a id="verify"></a>
## Verify

```bash
curl -s http://localhost:8000/api/dashboard -H "Authorization: Bearer $TOKEN"
```
Expected: JSON with admin fields (`total_learners`, `total_courses`, `active_courses`, `completed_courses`, `certificates`) or learner fields (`assigned_courses`, `in_progress`, `completed`, `certificates`).

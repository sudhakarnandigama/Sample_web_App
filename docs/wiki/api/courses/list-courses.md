# GET /api/courses — list courses

> **Sources** — `Proposal/Documentation/project_documentation.md:661-665`; [data/courses.md](../../data/courses.md); [auth/02-scopes.md](../../auth/02-scopes.md#courses-read)
> **Status** — [spec]
> **Page-size budget** — used 40 / 300 lines

<a id="purpose"></a>
## Purpose
Returns every course.

<a id="auth"></a>
## Auth
- Required header: `Authorization: Bearer <jwt>`
- Required scope: `courses:read` — [auth/02-scopes.md#courses-read](../../auth/02-scopes.md#courses-read)

<a id="request"></a>
## Request
No parameters.

<a id="responses"></a>
## Responses

### 200 OK
```json
[
  { "id": 1, "title": "Python Fundamentals", "description": "Python basics", "duration_hours": 8, "status": "ACTIVE", "created_at": "2026-08-24T10:00:00Z" }
]
```

### 401 Unauthorized
`MISSING_AUTH` | `INVALID_TOKEN`

### 403 Forbidden
`INSUFFICIENT_SCOPE`

<a id="side-effects"></a>
## Side effects
None — reads [data/courses.md](../../data/courses.md).

<a id="implementation"></a>
## Implementation
- Handler: `backend/app/routers/courses.py` `[planned]`

<a id="test-plan"></a>
## Test plan
| # | Case | Expected |
|---|---|---|
| 1 | ADMIN token | 200 array |
| 2 | LEARNER token | 200 array |
| 3 | no token | 401 `MISSING_AUTH` |

<a id="verify"></a>
## Verify

```bash
curl -s http://localhost:8000/api/courses -H "Authorization: Bearer $TOKEN"
```
Expected: HTTP 200, JSON array.

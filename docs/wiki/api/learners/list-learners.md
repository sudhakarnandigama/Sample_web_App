# GET /api/learners — list learners

> **Sources** — `Proposal/Documentation/project_documentation.md:695-699`; [data/learners.md](../../data/learners.md); [auth/02-scopes.md](../../auth/02-scopes.md#learners-read)
> **Status** — [spec]
> **Page-size budget** — used 39 / 300 lines

<a id="purpose"></a>
## Purpose
Returns every learner. Admin only.

<a id="auth"></a>
## Auth
- Required header: `Authorization: Bearer <jwt>`
- Required scope: `learners:read` — [auth/02-scopes.md#learners-read](../../auth/02-scopes.md#learners-read)

<a id="request"></a>
## Request
No parameters.

<a id="responses"></a>
## Responses

### 200 OK
```json
[
  { "id": 1, "user_id": 2, "name": "John Doe", "email": "john@example.com", "department": "IT", "status": "ACTIVE", "created_at": "2026-08-24T10:00:00Z" }
]
```

### 401 Unauthorized
`MISSING_AUTH` | `INVALID_TOKEN`

### 403 Forbidden
`INSUFFICIENT_SCOPE` — caller is `LEARNER`.

<a id="side-effects"></a>
## Side effects
None.

<a id="implementation"></a>
## Implementation
- Handler: `backend/app/routers/learners.py` `[planned]`

<a id="test-plan"></a>
## Test plan
| # | Case | Expected |
|---|---|---|
| 1 | ADMIN token | 200 array |
| 2 | LEARNER token | 403 `INSUFFICIENT_SCOPE` |
| 3 | no token | 401 `MISSING_AUTH` |

<a id="verify"></a>
## Verify

```bash
curl -s http://localhost:8000/api/learners -H "Authorization: Bearer $ADMIN_TOKEN"
```
Expected: HTTP 200, JSON array.

# POST /api/learners — create learner

> **Sources** — `Proposal/Documentation/project_documentation.md:707-711`; [data/learners.md](../../data/learners.md); [auth/02-scopes.md](../../auth/02-scopes.md#learners-write)
> **Status** — [spec]
> **Page-size budget** — used 49 / 300 lines

<a id="purpose"></a>
## Purpose
Creates a learner. Admin only.

<a id="auth"></a>
## Auth
- Required header: `Authorization: Bearer <jwt>`
- Required scope: `learners:write` — [auth/02-scopes.md#learners-write](../../auth/02-scopes.md#learners-write)

<a id="request"></a>
## Request

### Body
| Field | Type | Required | Constraints | Default |
|---|---|---|---|---|
| name | string | yes | non-empty; max 100 chars | — |
| email | string | yes | RFC 5322; max 254 chars | — |
| department | string | yes | non-empty; max 100 chars | — |

Schema source: `backend/app/schemas/learner.py` `[planned]`

<a id="responses"></a>
## Responses

### 201 Created
```json
{ "id": 6, "user_id": null, "name": "Anjali Rao", "email": "anjali@example.com", "department": "HR", "status": "ACTIVE", "created_at": "2026-08-24T10:00:00Z" }
```

### 400 Bad Request
`INVALID_LEARNER` — a required field empty or `email` malformed.

### 409 Conflict
`EMAIL_EXISTS` — another learner already has this `email`.

### 401 Unauthorized
`MISSING_AUTH` | `INVALID_TOKEN`

### 403 Forbidden
`INSUFFICIENT_SCOPE`

<a id="side-effects"></a>
## Side effects
1. Insert into `learners` → [data/learners.md#write-patterns](../../data/learners.md#write-patterns).

<a id="implementation"></a>
## Implementation
- Handler: `backend/app/routers/learners.py` `[planned]`

<a id="test-plan"></a>
## Test plan
| # | Case | Expected |
|---|---|---|
| 1 | ADMIN, valid body | 201, `user_id` = null |
| 2 | duplicate email | 409 `EMAIL_EXISTS` |
| 3 | empty name | 400 `INVALID_LEARNER` |

<a id="verify"></a>
## Verify

```bash
curl -s -X POST http://localhost:8000/api/learners -H "Authorization: Bearer $ADMIN_TOKEN" -H "Content-Type: application/json" -d '{"name":"Anjali Rao","email":"anjali@example.com","department":"HR"}'
```
Expected: HTTP 201, body has `id`, `status` = `ACTIVE`.

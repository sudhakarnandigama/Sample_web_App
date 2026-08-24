# PUT /api/learners/{id} — update learner

> **Sources** — `Proposal/Documentation/project_documentation.md:713-717`; [data/learners.md](../../data/learners.md); [auth/02-scopes.md](../../auth/02-scopes.md#learners-write)
> **Status** — [spec]
> **Page-size budget** — used 48 / 300 lines

<a id="purpose"></a>
## Purpose
Updates learner fields. Admin only.

<a id="auth"></a>
## Auth
- Required header: `Authorization: Bearer <jwt>`
- Required scope: `learners:write` — [auth/02-scopes.md#learners-write](../../auth/02-scopes.md#learners-write)

<a id="request"></a>
## Request

### Path parameters
| Param | Type | Required |
|---|---|---|
| id | integer | yes |

### Body (partial update — any subset)
| Field | Type | Required | Constraints |
|---|---|---|---|
| name | string | no | non-empty; max 100 chars |
| email | string | no | RFC 5322; max 254 chars |
| department | string | no | non-empty; max 100 chars |
| status | string | no | `ACTIVE` \| `INACTIVE` |

<a id="responses"></a>
## Responses

### 200 OK
```json
{ "id": 1, "user_id": 2, "name": "John Doe", "email": "john@example.com", "department": "IT", "status": "INACTIVE", "created_at": "2026-08-24T10:00:00Z" }
```

### 400 Bad Request
`INVALID_LEARNER` — a supplied field failed its constraint.

### 404 Not Found
`LEARNER_NOT_FOUND`

### 409 Conflict
`EMAIL_EXISTS` — `email` belongs to another learner.

### 401 Unauthorized
`MISSING_AUTH` | `INVALID_TOKEN`

### 403 Forbidden
`INSUFFICIENT_SCOPE`

<a id="side-effects"></a>
## Side effects
1. Update row in `learners` → [data/learners.md#write-patterns](../../data/learners.md#write-patterns).

<a id="implementation"></a>
## Implementation
- Handler: `backend/app/routers/learners.py` `[planned]`

<a id="test-plan"></a>
## Test plan
| # | Case | Expected |
|---|---|---|
| 1 | ADMIN sets `status` = `INACTIVE` | 200 |
| 2 | change email to an existing one | 409 `EMAIL_EXISTS` |
| 3 | unknown id | 404 `LEARNER_NOT_FOUND` |

<a id="verify"></a>
## Verify

```bash
curl -s -X PUT http://localhost:8000/api/learners/1 -H "Authorization: Bearer $ADMIN_TOKEN" -H "Content-Type: application/json" -d '{"status":"INACTIVE"}'
```
Expected: HTTP 200, `status` = `INACTIVE`.

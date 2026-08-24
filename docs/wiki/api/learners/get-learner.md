# GET /api/learners/{id} — get learner

> **Sources** — `Proposal/Documentation/project_documentation.md:701-705`; [data/learners.md](../../data/learners.md); [auth/02-scopes.md](../../auth/02-scopes.md#learners-read)
> **Status** — [spec]
> **Page-size budget** — used 41 / 300 lines

<a id="purpose"></a>
## Purpose
Returns one learner by id. Admin only.

<a id="auth"></a>
## Auth
- Required header: `Authorization: Bearer <jwt>`
- Required scope: `learners:read` — [auth/02-scopes.md#learners-read](../../auth/02-scopes.md#learners-read)

<a id="request"></a>
## Request

### Path parameters
| Param | Type | Required |
|---|---|---|
| id | integer | yes |

<a id="responses"></a>
## Responses

### 200 OK
```json
{ "id": 1, "user_id": 2, "name": "John Doe", "email": "john@example.com", "department": "IT", "status": "ACTIVE", "created_at": "2026-08-24T10:00:00Z" }
```

### 404 Not Found
`LEARNER_NOT_FOUND`

### 401 Unauthorized
`MISSING_AUTH` | `INVALID_TOKEN`

### 403 Forbidden
`INSUFFICIENT_SCOPE`

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
| 1 | existing id | 200 |
| 2 | unknown id | 404 `LEARNER_NOT_FOUND` |

<a id="verify"></a>
## Verify

```bash
curl -s http://localhost:8000/api/learners/1 -H "Authorization: Bearer $ADMIN_TOKEN"
```
Expected: HTTP 200 with `id` = 1, or 404 `LEARNER_NOT_FOUND`.

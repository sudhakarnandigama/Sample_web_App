# PUT /api/courses/{id} — update course

> **Sources** — `Proposal/Documentation/project_documentation.md:679-683`; [data/courses.md](../../data/courses.md); [auth/02-scopes.md](../../auth/02-scopes.md#courses-write)
> **Status** — [spec]
> **Page-size budget** — used 50 / 300 lines

<a id="purpose"></a>
## Purpose
Updates course fields, including activate/deactivate via `status`.

<a id="auth"></a>
## Auth
- Required header: `Authorization: Bearer <jwt>`
- Required scope: `courses:write` — [auth/02-scopes.md#courses-write](../../auth/02-scopes.md#courses-write)

<a id="request"></a>
## Request

### Path parameters
| Param | Type | Required |
|---|---|---|
| id | integer | yes |

### Body (partial update — any subset)
| Field | Type | Required | Constraints |
|---|---|---|---|
| title | string | no | non-empty; max 200 chars |
| description | string | no | non-empty |
| duration_hours | integer | no | > 0 |
| status | string | no | `ACTIVE` \| `INACTIVE` |

<a id="responses"></a>
## Responses

### 200 OK
```json
{ "id": 1, "title": "Python Fundamentals", "description": "updated", "duration_hours": 8, "status": "ACTIVE", "created_at": "2026-08-24T10:00:00Z" }
```

### 400 Bad Request
`INVALID_COURSE` — a supplied field failed its constraint.

### 404 Not Found
`COURSE_NOT_FOUND`

### 401 Unauthorized
`MISSING_AUTH` | `INVALID_TOKEN`

### 403 Forbidden
`INSUFFICIENT_SCOPE`

<a id="side-effects"></a>
## Side effects
1. Update row in `courses` → [data/courses.md#write-patterns](../../data/courses.md#write-patterns).

<a id="implementation"></a>
## Implementation
- Handler: `backend/app/routers/courses.py` `[planned]`

<a id="test-plan"></a>
## Test plan
| # | Case | Expected |
|---|---|---|
| 1 | ADMIN sets `status` = `INACTIVE` | 200, status changed |
| 2 | unknown id | 404 `COURSE_NOT_FOUND` |
| 3 | `duration_hours` = -1 | 400 `INVALID_COURSE` |

<a id="verify"></a>
## Verify

```bash
curl -s -X PUT http://localhost:8000/api/courses/1 -H "Authorization: Bearer $ADMIN_TOKEN" -H "Content-Type: application/json" -d '{"status":"INACTIVE"}'
```
Expected: HTTP 200, `status` = `INACTIVE`.

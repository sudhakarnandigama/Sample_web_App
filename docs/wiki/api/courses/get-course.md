# GET /api/courses/{id} — get course

> **Sources** — `Proposal/Documentation/project_documentation.md:667-671`; [data/courses.md](../../data/courses.md); [auth/02-scopes.md](../../auth/02-scopes.md#courses-read)
> **Status** — [spec]
> **Page-size budget** — used 43 / 300 lines

<a id="purpose"></a>
## Purpose
Returns one course by id.

<a id="auth"></a>
## Auth
- Required header: `Authorization: Bearer <jwt>`
- Required scope: `courses:read` — [auth/02-scopes.md#courses-read](../../auth/02-scopes.md#courses-read)

<a id="request"></a>
## Request

### Path parameters
| Param | Type | Required | Notes |
|---|---|---|---|
| id | integer | yes | course id |

<a id="responses"></a>
## Responses

### 200 OK
```json
{ "id": 1, "title": "Python Fundamentals", "description": "Python basics", "duration_hours": 8, "status": "ACTIVE", "created_at": "2026-08-24T10:00:00Z" }
```

### 404 Not Found
```json
{ "error": { "code": "COURSE_NOT_FOUND", "message": "no course with id <id>" } }
```

### 401 Unauthorized
`MISSING_AUTH` | `INVALID_TOKEN`

### 403 Forbidden
`INSUFFICIENT_SCOPE`

<a id="side-effects"></a>
## Side effects
None.

<a id="implementation"></a>
## Implementation
- Handler: `backend/app/routers/courses.py` `[planned]`

<a id="test-plan"></a>
## Test plan
| # | Case | Expected |
|---|---|---|
| 1 | existing id | 200 |
| 2 | unknown id | 404 `COURSE_NOT_FOUND` |
| 3 | non-integer id | 422 validation error |

<a id="verify"></a>
## Verify

```bash
curl -s http://localhost:8000/api/courses/1 -H "Authorization: Bearer $TOKEN"
```
Expected: HTTP 200 with `id` = 1, or 404 `COURSE_NOT_FOUND`.

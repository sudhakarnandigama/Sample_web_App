# POST /api/courses — create course

> **Sources** — `Proposal/Documentation/project_documentation.md:673-677`; [data/courses.md](../../data/courses.md); [auth/02-scopes.md](../../auth/02-scopes.md#courses-write)
> **Status** — [spec]
> **Page-size budget** — used 51 / 300 lines

<a id="purpose"></a>
## Purpose
Creates a course. Requires the admin role.

<a id="auth"></a>
## Auth
- Required header: `Authorization: Bearer <jwt>`
- Required scope: `courses:write` — [auth/02-scopes.md#courses-write](../../auth/02-scopes.md#courses-write)

<a id="request"></a>
## Request

### Body
| Field | Type | Required | Constraints | Default |
|---|---|---|---|---|
| title | string | yes | non-empty; max 200 chars | — |
| description | string | yes | non-empty | — |
| duration_hours | integer | yes | > 0 | — |

Schema source: `backend/app/schemas/course.py` `[planned]`

<a id="responses"></a>
## Responses

### 201 Created
```json
{ "id": 4, "title": "Web Development Basics", "description": "HTML/CSS/JS", "duration_hours": 12, "status": "ACTIVE", "created_at": "2026-08-24T10:00:00Z" }
```

### 400 Bad Request
`INVALID_COURSE` — `title`/`description` empty, or `duration_hours` ≤ 0.

### 401 Unauthorized
`MISSING_AUTH` | `INVALID_TOKEN`

### 403 Forbidden
`INSUFFICIENT_SCOPE` — caller is `LEARNER`.

<a id="side-effects"></a>
## Side effects
1. Insert into `courses` → [data/courses.md#write-patterns](../../data/courses.md#write-patterns).

<a id="implementation"></a>
## Implementation
- Handler: `backend/app/routers/courses.py` `[planned]`

<a id="test-plan"></a>
## Test plan
| # | Case | Expected |
|---|---|---|
| 1 | ADMIN, valid body | 201, `status` = `ACTIVE` |
| 2 | empty title | 400 `INVALID_COURSE` |
| 3 | `duration_hours` = 0 | 400 `INVALID_COURSE` |
| 4 | LEARNER token | 403 `INSUFFICIENT_SCOPE` |

<a id="verify"></a>
## Verify

```bash
curl -s -X POST http://localhost:8000/api/courses -H "Authorization: Bearer $ADMIN_TOKEN" -H "Content-Type: application/json" -d '{"title":"Web Development Basics","description":"HTML/CSS/JS","duration_hours":12}'
```
Expected: HTTP 201, body has `id`, `status` = `ACTIVE`.

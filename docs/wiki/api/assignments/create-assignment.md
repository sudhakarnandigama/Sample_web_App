# POST /api/assignments — assign course

> **Sources** — `Proposal/Documentation/project_documentation.md:727-743`; [data/course_assignments.md](../../data/course_assignments.md); [auth/02-scopes.md](../../auth/02-scopes.md#assignments-write)
> **Status** — [spec]
> **Page-size budget** — used 48 / 300 lines

<a id="purpose"></a>
## Purpose
Assigns a course to a learner. Admin only.

<a id="auth"></a>
## Auth
- Required header: `Authorization: Bearer <jwt>`
- Required scope: `assignments:write` — [auth/02-scopes.md#assignments-write](../../auth/02-scopes.md#assignments-write)

<a id="request"></a>
## Request

### Body
| Field | Type | Required | Constraints | Default |
|---|---|---|---|---|
| learner_id | integer | yes | references `learners.id` | — |
| course_id | integer | yes | references `courses.id` | — |

Schema source: `backend/app/schemas/assignment.py` `[planned]`

<a id="responses"></a>
## Responses

### 201 Created
```json
{ "id": 1, "course_id": 2, "learner_id": 1, "progress": 0, "status": "NOT_STARTED", "assigned_date": "2026-08-24T10:00:00Z" }
```

### 404 Not Found
`LEARNER_NOT_FOUND` | `COURSE_NOT_FOUND`

### 409 Conflict
`ASSIGNMENT_EXISTS` — the course is already assigned to this learner.

### 401 Unauthorized
`MISSING_AUTH` | `INVALID_TOKEN`

### 403 Forbidden
`INSUFFICIENT_SCOPE`

<a id="side-effects"></a>
## Side effects
1. Insert into `course_assignments` → [data/course_assignments.md#write-patterns](../../data/course_assignments.md#write-patterns).

<a id="implementation"></a>
## Implementation
- Handler: `backend/app/routers/assignments.py` `[planned]`

<a id="test-plan"></a>
## Test plan
| # | Case | Expected |
|---|---|---|
| 1 | ADMIN, new pair | 201, `progress` = 0, `status` = `NOT_STARTED` |
| 2 | same pair again | 409 `ASSIGNMENT_EXISTS` |
| 3 | unknown learner_id | 404 `LEARNER_NOT_FOUND` |

<a id="verify"></a>
## Verify

```bash
curl -s -X POST http://localhost:8000/api/assignments -H "Authorization: Bearer $ADMIN_TOKEN" -H "Content-Type: application/json" -d '{"learner_id":1,"course_id":2}'
```
Expected: HTTP 201, `progress` = 0, `status` = `NOT_STARTED`.

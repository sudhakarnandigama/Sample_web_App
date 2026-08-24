# PUT /api/assignments/{id}/progress — update progress

> **Sources** — `Proposal/Documentation/project_documentation.md:744-757`; [data/course_assignments.md](../../data/course_assignments.md); [auth/02-scopes.md](../../auth/02-scopes.md#progress-write-own)
> **Status** — [spec]
> **Page-size budget** — used 49 / 300 lines

<a id="purpose"></a>
## Purpose
Updates a learner's own progress percentage and status on an assignment.

<a id="auth"></a>
## Auth
- Required header: `Authorization: Bearer <jwt>`
- Required scope: `progress:write:own` — [auth/02-scopes.md#progress-write-own](../../auth/02-scopes.md#progress-write-own)
- Ownership: the assignment's `learner_id` must equal the caller's `learners.user_id`-resolved learner.

<a id="request"></a>
## Request

### Path parameters
| Param | Type | Required |
|---|---|---|
| id | integer | yes |

### Body
| Field | Type | Required | Constraints | Default |
|---|---|---|---|---|
| progress | integer | yes | `0..100` | — |
| status | string | no | `NOT_STARTED` \| `IN_PROGRESS` \| `COMPLETED` | derived if omitted |

Status derivation when omitted: `progress = 100` ⇒ `COMPLETED`; `progress > 0` ⇒ `IN_PROGRESS`; `progress = 0` ⇒ `NOT_STARTED`.

<a id="responses"></a>
## Responses

### 200 OK
```json
{ "id": 1, "course_id": 2, "learner_id": 1, "progress": 75, "status": "IN_PROGRESS", "assigned_date": "2026-08-24T10:00:00Z" }
```

### 400 Bad Request
`INVALID_PROGRESS` — `progress` outside `0..100`, or `status` inconsistent with `progress`.

### 404 Not Found
`ASSIGNMENT_NOT_FOUND`

### 403 Forbidden
`INSUFFICIENT_SCOPE` — caller is `ADMIN`, or the assignment belongs to another learner.

### 401 Unauthorized
`MISSING_AUTH` | `INVALID_TOKEN`

<a id="side-effects"></a>
## Side effects
1. Update row in `course_assignments` → [data/course_assignments.md#write-patterns](../../data/course_assignments.md#write-patterns).

<a id="implementation"></a>
## Implementation
- Handler: `backend/app/routers/assignments.py` `[planned]`

<a id="test-plan"></a>
## Test plan
| # | Case | Expected |
|---|---|---|
| 1 | owner, `progress` = 75 | 200, `status` = `IN_PROGRESS` |
| 2 | owner, `progress` = 100 | 200, `status` = `COMPLETED` |
| 3 | `progress` = 120 | 400 `INVALID_PROGRESS` |
| 4 | different learner's assignment | 403 `INSUFFICIENT_SCOPE` |

<a id="verify"></a>
## Verify

```bash
curl -s -X PUT http://localhost:8000/api/assignments/1/progress -H "Authorization: Bearer $LEARNER_TOKEN" -H "Content-Type: application/json" -d '{"progress":75}'
```
Expected: HTTP 200, `progress` = 75, `status` = `IN_PROGRESS`.

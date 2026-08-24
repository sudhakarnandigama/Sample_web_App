# DELETE /api/learners/{id} — delete learner

> **Sources** — `Proposal/Documentation/project_documentation.md:719-723`; [data/learners.md](../../data/learners.md); [auth/02-scopes.md](../../auth/02-scopes.md#learners-write)
> **Status** — [spec]
> **Page-size budget** — used 39 / 300 lines

<a id="purpose"></a>
## Purpose
Deletes a learner (hard delete). Admin only.

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

<a id="responses"></a>
## Responses

### 204 No Content
Empty body.

### 404 Not Found
`LEARNER_NOT_FOUND`

### 401 Unauthorized
`MISSING_AUTH` | `INVALID_TOKEN`

### 403 Forbidden
`INSUFFICIENT_SCOPE`

<a id="side-effects"></a>
## Side effects
1. Delete row from `learners`. Rows in `course_assignments`, `assessment_attempts`, and `certificates` referencing it are deleted by ORM cascade `[planned]`.

<a id="implementation"></a>
## Implementation
- Handler: `backend/app/routers/learners.py` `[planned]`

<a id="test-plan"></a>
## Test plan
| # | Case | Expected |
|---|---|---|
| 1 | existing id | 204 |
| 2 | unknown id | 404 `LEARNER_NOT_FOUND` |

<a id="verify"></a>
## Verify

```bash
curl -s -o /dev/null -w "%{http_code}" -X DELETE http://localhost:8000/api/learners/6 -H "Authorization: Bearer $ADMIN_TOKEN"
```
Expected: `204`.

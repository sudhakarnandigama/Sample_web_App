# DELETE /api/courses/{id} — delete course

> **Sources** — `Proposal/Documentation/project_documentation.md:685-689`; [data/courses.md](../../data/courses.md); [auth/02-scopes.md](../../auth/02-scopes.md#courses-write)
> **Status** — [spec]
> **Page-size budget** — used 40 / 300 lines

<a id="purpose"></a>
## Purpose
Deletes a course (hard delete).

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

<a id="responses"></a>
## Responses

### 204 No Content
Empty body.

### 404 Not Found
`COURSE_NOT_FOUND`

### 401 Unauthorized
`MISSING_AUTH` | `INVALID_TOKEN`

### 403 Forbidden
`INSUFFICIENT_SCOPE`

<a id="side-effects"></a>
## Side effects
1. Delete row from `courses`. Rows in `course_assignments`, `assessments`, and `certificates` referencing it are deleted by the ORM's `ondelete` cascade `[planned]`.

<a id="implementation"></a>
## Implementation
- Handler: `backend/app/routers/courses.py` `[planned]`

<a id="test-plan"></a>
## Test plan
| # | Case | Expected |
|---|---|---|
| 1 | existing id | 204 |
| 2 | unknown id | 404 `COURSE_NOT_FOUND` |

<a id="verify"></a>
## Verify

```bash
curl -s -o /dev/null -w "%{http_code}" -X DELETE http://localhost:8000/api/courses/4 -H "Authorization: Bearer $ADMIN_TOKEN"
```
Expected: `204`.

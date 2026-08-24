# Route: /courses — Courses list

> **Sources** — `Proposal/Documentation/project_documentation.md:165-193`; [api/courses/list-courses.md](../api/courses/list-courses.md)
> **Status** — [spec]
> **Page-size budget** — used 39 / 300 lines

<a id="purpose"></a>
## Purpose
Admin lists all courses with add/edit/delete/activate actions.

<a id="route"></a>
## Route
- Path: `/courses`
- File: `frontend/src/app/features/courses/courses.component.ts` `[planned]`
- Auth required: yes (`courses:read`; admin-only actions need `courses:write`)

<a id="state"></a>
## Local state
| Name | Type | Initial | Updated by |
|---|---|---|---|
| courses | array | [] | GET `/api/courses` response |

<a id="behavior"></a>
## Behavior
1. On init: GET `/api/courses` per [api/courses/list-courses.md](../api/courses/list-courses.md).
2. "Add" → navigate `/courses/new`.
3. Row edit → `/courses/:id/edit`.
4. Delete → confirmation dialog → DELETE `/api/courses/{id}` per [api/courses/delete-course.md](../api/courses/delete-course.md).
5. Activate/deactivate → PUT `/api/courses/{id}` with `status` per [api/courses/update-course.md](../api/courses/update-course.md).

<a id="components"></a>
## Components used
- `<DataTable>`, `<StatusBadge>`, `<ConfirmationDialog>` — `frontend/src/app/shared/**` `[planned]`

<a id="test-plan"></a>
## Test plan
| # | Case | Expected |
|---|---|---|
| 1 | admin opens /courses | list loads |
| 2 | delete confirmed | row removed, DELETE 204 |
| 3 | deactivate | status badge shows `INACTIVE` |

<a id="verify"></a>
## Verify

```bash
curl -s http://localhost:8000/api/courses -H "Authorization: Bearer $ADMIN_TOKEN"
```
Expected: HTTP 200, JSON array rendered by the page.

# Route: /assignments — Course assignments

> **Sources** — `Proposal/Documentation/project_documentation.md:229-253`; [api/assignments/create-assignment.md](../api/assignments/create-assignment.md)
> **Status** — [spec]
> **Page-size budget** — used 39 / 300 lines

<a id="purpose"></a>
## Purpose
Admin assigns courses to learners and sees existing assignments.

<a id="route"></a>
## Route
- Path: `/assignments`
- File: `frontend/src/app/features/assignments/assignments.component.ts` `[planned]`
- Auth required: yes (`assignments:write`)

<a id="state"></a>
## Local state
| Name | Type | Initial | Updated by |
|---|---|---|---|
| learner_id | number \| null | null | selector change |
| course_id | number \| null | null | selector change |
| error | string \| null | null | API error |

<a id="behavior"></a>
## Behavior
1. Load learners via [api/learners/list-learners.md](../api/learners/list-learners.md) and courses via [api/courses/list-courses.md](../api/courses/list-courses.md) to populate selectors.
2. Submit → POST `/api/assignments` per [api/assignments/create-assignment.md](../api/assignments/create-assignment.md).
3. On 201: show success, clear form.
4. On 409 `ASSIGNMENT_EXISTS`: show "Course already assigned to this learner".

<a id="components"></a>
## Components used
- `<Select>`, `<Button>`, `<ErrorBanner>` — `frontend/src/app/shared/**` `[planned]`

<a id="test-plan"></a>
## Test plan
| # | Case | Expected |
|---|---|---|
| 1 | select learner + course, assign | POST 201 |
| 2 | same pair again | "Course already assigned" banner |

<a id="verify"></a>
## Verify

```bash
curl -s -X POST http://localhost:8000/api/assignments -H "Authorization: Bearer $ADMIN_TOKEN" -H "Content-Type: application/json" -d '{"learner_id":1,"course_id":2}'
```
Expected: HTTP 201.

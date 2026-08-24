# Route: /reports — Reports

> **Sources** — `Proposal/Documentation/project_documentation.md:342-368`; [api/learners/list-learners.md](../api/learners/list-learners.md); [api/courses/list-courses.md](../api/courses/list-courses.md)
> **Status** — [spec]
> **Page-size budget** — used 40 / 300 lines

<a id="purpose"></a>
## Purpose
Admin views two basic reports: learner report and course report. Computed on the frontend from existing read endpoints — there is no dedicated reports API in PRD §18–24. `[GAP-REP-01: no reports API — resolved as frontend aggregation from GET endpoints]`

<a id="route"></a>
## Route
- Path: `/reports`
- File: `frontend/src/app/features/reports/reports.component.ts` `[planned]`
- Auth required: yes (`reports:read`, admin)

<a id="state"></a>
## Local state
| Name | Type | Initial | Updated by |
|---|---|---|---|
| learnerReport | array | [] | aggregation of learners + assignments + attempts |
| courseReport | array | [] | aggregation of courses + assignments |

<a id="behavior"></a>
## Behavior
1. Load [api/learners/list-learners.md](../api/learners/list-learners.md), [api/courses/list-courses.md](../api/courses/list-courses.md), [api/certificates/list-certificates.md](../api/certificates/list-certificates.md).
2. **Learner report** columns: Learner, Course, Progress, Assessment Score, Status.
3. **Course report** columns: Course, Total Learners, Completed, In Progress, Not Started (from `course_assignments.status`).

<a id="components"></a>
## Components used
- `<DataTable>` — `frontend/src/app/shared/**` `[planned]`

<a id="test-plan"></a>
## Test plan
| # | Case | Expected |
|---|---|---|
| 1 | admin opens /reports | learner + course tables render |
| 2 | learner role opens /reports | guard blocks, redirect |

<a id="verify"></a>
## Verify

```bash
curl -s http://localhost:8000/api/learners -H "Authorization: Bearer $ADMIN_TOKEN" && curl -s http://localhost:8000/api/courses -H "Authorization: Bearer $ADMIN_TOKEN"
```
Expected: two JSON arrays feeding the report tables.

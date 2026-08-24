# Route: /courses/:id — Course details

> **Sources** — `Proposal/Documentation/project_documentation.md:1020-1039`; [api/courses/get-course.md](../api/courses/get-course.md)
> **Status** — [spec]
> **Page-size budget** — used 37 / 300 lines

<a id="purpose"></a>
## Purpose
Shows one course's fields, and for a learner, its progress and entry point to the assessment.

<a id="route"></a>
## Route
- Path: `/courses/:id`
- File: `frontend/src/app/features/courses/course-details.component.ts` `[planned]`
- Auth required: yes (`courses:read`)

<a id="state"></a>
## Local state
| Name | Type | Initial | Updated by |
|---|---|---|---|
| course | object \| null | null | GET `/api/courses/{id}` response |

<a id="behavior"></a>
## Behavior
1. On init: GET `/api/courses/{id}` per [api/courses/get-course.md](../api/courses/get-course.md).
2. Learner with this course assigned: show "Take assessment" → `/assessment/:courseId`.
3. 404 `COURSE_NOT_FOUND`: show "Course not found".

<a id="components"></a>
## Components used
- `<Card>`, `<Button>` — `frontend/src/app/shared/**` `[planned]`

<a id="test-plan"></a>
## Test plan
| # | Case | Expected |
|---|---|---|
| 1 | existing id | course fields shown |
| 2 | unknown id | "Course not found" |

<a id="verify"></a>
## Verify

```bash
curl -s http://localhost:8000/api/courses/1 -H "Authorization: Bearer $TOKEN"
```
Expected: HTTP 200 with course fields.

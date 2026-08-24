# Route: /courses/new & /courses/:id/edit — Course form

> **Sources** — `Proposal/Documentation/project_documentation.md:165-193`; [api/courses/create-course.md](../api/courses/create-course.md); [api/courses/update-course.md](../api/courses/update-course.md)
> **Status** — [spec]
> **Page-size budget** — used 40 / 300 lines

<a id="purpose"></a>
## Purpose
Admin creates or edits a course.

<a id="route"></a>
## Route
- Path: `/courses/new` (create), `/courses/:id/edit` (edit)
- File: `frontend/src/app/features/courses/course-form.component.ts` `[planned]`
- Auth required: yes (`courses:write`)

<a id="state"></a>
## Local state
| Name | Type | Initial | Updated by |
|---|---|---|---|
| title | string | "" (edit: loaded) | input change |
| description | string | "" (edit: loaded) | input change |
| duration_hours | number | null | input change |
| isSubmitting | boolean | false | submit start/end |
| error | string \| null | null | API error |

<a id="behavior"></a>
## Behavior
1. Edit mode: GET `/api/courses/{id}` to prefill.
2. Validate: `title`, `description`, `duration_hours` required; `duration_hours > 0`.
3. Create → POST `/api/courses` per [api/courses/create-course.md](../api/courses/create-course.md); Edit → PUT per [api/courses/update-course.md](../api/courses/update-course.md).
4. On 201/200: navigate `/courses`.
5. On 400 `INVALID_COURSE`: show inline errors.

<a id="components"></a>
## Components used
- `<TextField>`, `<TextArea>`, `<NumberField>`, `<Button>` — `frontend/src/app/shared/**` `[planned]`

<a id="test-plan"></a>
## Test plan
| # | Case | Expected |
|---|---|---|
| 1 | valid create | POST 201, navigate /courses |
| 2 | empty title | inline "Title - Required" |
| 3 | edit and save | PUT 200 |

<a id="verify"></a>
## Verify

```bash
curl -s -X POST http://localhost:8000/api/courses -H "Authorization: Bearer $ADMIN_TOKEN" -H "Content-Type: application/json" -d '{"title":"Web Development Basics","description":"HTML/CSS/JS","duration_hours":12}'
```
Expected: HTTP 201.

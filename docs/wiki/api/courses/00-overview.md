# Resource: courses

> **Sources** — interview Q2; `Proposal/Documentation/project_documentation.md:165-193,659-689`
> **Status** — [spec]
> **Page-size budget** — used 26 / 200 lines

Course CRUD + activate/deactivate. Course schema: [data/courses.md](../../data/courses.md).

| Method | Path | Endpoint page | Scope |
|---|---|---|---|
| GET | `/api/courses` | [list-courses.md](list-courses.md) | `courses:read` |
| GET | `/api/courses/{id}` | [get-course.md](get-course.md) | `courses:read` |
| POST | `/api/courses` | [create-course.md](create-course.md) | `courses:write` |
| PUT | `/api/courses/{id}` | [update-course.md](update-course.md) | `courses:write` |
| DELETE | `/api/courses/{id}` | [delete-course.md](delete-course.md) | `courses:write` |

Course object: `{ "id", "title", "description", "duration_hours", "status", "created_at" }` — see [data/courses.md#columns](../../data/courses.md#columns).

<a id="verify"></a>
## Verify

```bash
curl -s http://localhost:8000/api/courses -H "Authorization: Bearer $TOKEN"
```
Expected: HTTP 200, JSON array of course objects.

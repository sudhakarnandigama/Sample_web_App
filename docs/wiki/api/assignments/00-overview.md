# Resource: assignments

> **Sources** — interview Q2; `Proposal/Documentation/project_documentation.md:229-253,727-757`
> **Status** — [spec]
> **Page-size budget** — used 25 / 200 lines

Course↔learner assignment + progress. Schema: [data/course_assignments.md](../../data/course_assignments.md).

| Method | Path | Endpoint page | Scope |
|---|---|---|---|
| POST | `/api/assignments` | [create-assignment.md](create-assignment.md) | `assignments:write` |
| PUT | `/api/assignments/{id}/progress` | [update-progress.md](update-progress.md) | `progress:write:own` |

Assignment object: `{ "id", "course_id", "learner_id", "progress", "status", "assigned_date" }` — see [data/course_assignments.md#columns](../../data/course_assignments.md#columns).

<a id="verify"></a>
## Verify

```bash
curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:8000/api/assignments -H "Authorization: Bearer $ADMIN_TOKEN" -H "Content-Type: application/json" -d '{"learner_id":1,"course_id":2}'
```
Expected: `201` (or `409` if already assigned).

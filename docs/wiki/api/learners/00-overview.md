# Resource: learners

> **Sources** — interview Q2; `Proposal/Documentation/project_documentation.md:196-225,693-723`
> **Status** — [spec]
> **Page-size budget** — used 26 / 200 lines

Learner CRUD. Learner schema: [data/learners.md](../../data/learners.md).

| Method | Path | Endpoint page | Scope |
|---|---|---|---|
| GET | `/api/learners` | [list-learners.md](list-learners.md) | `learners:read` |
| GET | `/api/learners/{id}` | [get-learner.md](get-learner.md) | `learners:read` |
| POST | `/api/learners` | [create-learner.md](create-learner.md) | `learners:write` |
| PUT | `/api/learners/{id}` | [update-learner.md](update-learner.md) | `learners:write` |
| DELETE | `/api/learners/{id}` | [delete-learner.md](delete-learner.md) | `learners:write` |

Learner object: `{ "id", "user_id", "name", "email", "department", "status", "created_at" }` — see [data/learners.md#columns](../../data/learners.md#columns).

<a id="verify"></a>
## Verify

```bash
curl -s http://localhost:8000/api/learners -H "Authorization: Bearer $ADMIN_TOKEN"
```
Expected: HTTP 200, JSON array of learner objects.

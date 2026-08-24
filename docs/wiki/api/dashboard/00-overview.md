# Resource: dashboard

> **Sources** — interview Q2; `Proposal/Documentation/project_documentation.md:127-163,639-655`
> **Status** — [spec]
> **Page-size budget** — used 21 / 200 lines

Role-dependent summary counts. Admin sees org-wide stats; learner sees own stats.

| Method | Path | Endpoint page |
|---|---|---|
| GET | `/api/dashboard` | [get-dashboard.md](get-dashboard.md) |

<a id="verify"></a>
## Verify

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/dashboard -H "Authorization: Bearer $TOKEN"
```
Expected: `200`.

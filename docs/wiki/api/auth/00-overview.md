# Resource: auth

> **Sources** — interview Q5; `Proposal/Documentation/project_documentation.md:621-637`
> **Status** — [spec]
> **Page-size budget** — used 22 / 200 lines

Login and token issuance. See [auth/00-overview.md](../../auth/00-overview.md) for the full flow.

| Method | Path | Endpoint page |
|---|---|---|
| POST | `/api/auth/login` | [login.md](login.md) |

<a id="verify"></a>
## Verify

```bash
curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:8000/api/auth/login -H "Content-Type: application/json" -d '{"username":"admin","password":"admin123"}'
```
Expected: `200`.

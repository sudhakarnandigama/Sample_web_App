# Operations — overview

> **Sources** — interview Q7; `Proposal/Documentation/project_documentation.md:880-1002`
> **Status** — [spec]
> **Page-size budget** — used 34 / 200 lines

<a id="environments"></a>
## Environments

| Env | Backend URL | Frontend URL | DB | Purpose |
|---|---|---|---|---|
| local | `http://localhost:8000` | `http://localhost:4200` | `backend/training_demo.db` | demo |

Single environment; no production deploy.

<a id="deploy-units"></a>
## Deploy units
- backend — FastAPI via `uvicorn app.main:app --reload` (see [start-backend.md](runbooks/start-backend.md))
- frontend — Angular via `ng serve` (see [start-frontend.md](runbooks/start-frontend.md))

<a id="config"></a>
## Config
All configuration: [env-vars.md](env-vars.md).

<a id="runbooks"></a>
## Runbooks
- [start-backend.md](runbooks/start-backend.md)
- [start-frontend.md](runbooks/start-frontend.md)
- [seed-data.md](runbooks/seed-data.md)

<a id="verify"></a>
## Verify

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs
```
Expected: `200`.

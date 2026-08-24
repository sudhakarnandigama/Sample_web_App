# Environment variables

> **Sources** — interview Q4, Q5, Q6; `Proposal/Documentation/project_documentation.md:880-925,978-1002`
> **Status** — [spec]
> **Page-size budget** — used 36 / 300 lines

| Variable | Service | Required | Default | Secret | Read at | Purpose |
|---|---|---|---|---|---|---|
| `DATABASE_URL` | backend | no | `sqlite:///./training_demo.db` | no | `backend/app/database.py` `[planned]` | SQLite connection string |
| `JWT_SECRET` | backend | yes | — | yes | `backend/app/auth.py` `[planned]` | JWT HS256 signing key |
| `JWT_ALGORITHM` | backend | no | `HS256` | no | `backend/app/auth.py` `[planned]` | JWT algorithm |
| `JWT_EXPIRE_MINUTES` | backend | no | `480` | no | `backend/app/auth.py` `[planned]` | token lifetime |
| `CORS_ORIGINS` | backend | no | `http://localhost:4200` | no | `backend/app/main.py` `[planned]` | allowed Angular dev origin |
| `apiUrl` | frontend | yes | `http://localhost:8000/api` | no | `frontend/src/environments/environment.ts` `[planned]` | API base URL (Angular environment constant, not a process env var) |

<a id="loading"></a>
## Loading
- Backend reads via `os.getenv` at `backend/app/config.py` `[planned]`; `JWT_SECRET` has no default and the app fails fast at startup if unset.
- Frontend: Angular loads `environment.ts` at build time; no runtime env vars.

<a id="verify"></a>
## Verify

```bash
python -c "import os; print('JWT_SECRET' in os.environ)"
```
Expected: `True` (after exporting `JWT_SECRET` before starting the backend).

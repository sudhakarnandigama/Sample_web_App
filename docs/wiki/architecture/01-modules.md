# Module map — monolith

> **Sources** — interview Q3, Q7; `Proposal/Documentation/project_documentation.md:372-459`
> **Status** — [spec]
> **Page-size budget** — used 40 / 300 lines

Single deploy: Angular frontend + FastAPI backend. No shared libraries between them; the contract between the two is [api/00-overview.md](../api/00-overview.md).

<a id="backend-modules"></a>
## Backend modules

| Module | File | Owns |
|---|---|---|
| entrypoint | `backend/app/main.py` | FastAPI app, router registration, CORS |
| database | `backend/app/database.py` | SQLAlchemy engine/session, `DATABASE_URL` |
| models | `backend/app/models/*.py` | SQLAlchemy ORM classes for the 8 tables in [data/00-overview.md](../data/00-overview.md) |
| schemas | `backend/app/schemas/*.py` | Pydantic request/response schemas |
| routers | `backend/app/routers/*.py` | one router per resource in [api/00-overview.md](../api/00-overview.md) |
| services | `backend/app/services/*.py` | auth, assessment scoring, certificate issuance |

All backend paths are `[planned]`.

<a id="frontend-modules"></a>
## Frontend modules

| Module | File | Owns |
|---|---|---|
| services | `frontend/src/app/core/services/*.ts` | HTTP calls to [api/00-overview.md](../api/00-overview.md) |
| guards | `frontend/src/app/core/guards/auth.guard.ts` | route protection by role |
| interceptors | `frontend/src/app/core/interceptors/auth.interceptor.ts` | attaches `Authorization: Bearer <jwt>` |
| shared | `frontend/src/app/shared/**` | navbar, sidebar, confirmation dialog |
| features | `frontend/src/app/features/**` | one folder per UI route in [ui/00-overview.md](../ui/00-overview.md) |
| routing | `frontend/src/app/app.routes.ts` | route table |
| bootstrap | `frontend/src/app/app.config.ts` | app config |

All frontend paths are `[planned]`.

<a id="verify"></a>
## Verify

```bash
find backend/app frontend/src/app -type f | wc -l
```
Expected: > 0 files (after implementation); matches the module list above.

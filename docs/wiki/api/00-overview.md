# API contracts — overview

> **Sources** — interview Q4, Q5; `Proposal/Documentation/project_documentation.md:613-818`
> **Status** — [spec]
> **Page-size budget** — used 44 / 200 lines

<a id="base-url"></a>
## Base URL
`http://localhost:8000/api`

Swagger UI: `http://localhost:8000/docs` (`Proposal/Documentation/project_documentation.md:943-945`).

<a id="headers"></a>
## Common headers
| Header | Required | Format |
|---|---|---|
| Authorization | yes (all except `POST /api/auth/login`) | `Bearer <jwt>` |
| Content-Type | yes (POST/PUT) | `application/json` |

<a id="error-envelope"></a>
## Error envelope
All error responses use one envelope:

```json
{ "error": { "code": "MISSING_AUTH", "message": "human-readable detail" } }
```

<a id="error-codes"></a>
## Common error codes
| Code | HTTP | Meaning |
|---|---|---|
| `MISSING_AUTH` | 401 | no `Authorization` header |
| `INVALID_TOKEN` | 401 | malformed / expired / bad-signature JWT |
| `INSUFFICIENT_SCOPE` | 403 | JWT role lacks the endpoint's required scope |

Resource-specific codes are documented on each endpoint page.

<a id="id-format"></a>
## ID format
All resource ids are positive integers (`INTEGER PRIMARY KEY AUTOINCREMENT`).

<a id="pagination"></a>
## Pagination
None — demo returns full lists. No `limit`/`offset` parameters.

<a id="resources"></a>
## Resources
| Resource | Overview |
|---|---|
| auth | [auth/00-overview.md](auth/00-overview.md) |
| dashboard | [dashboard/00-overview.md](dashboard/00-overview.md) |
| courses | [courses/00-overview.md](courses/00-overview.md) |
| learners | [learners/00-overview.md](learners/00-overview.md) |
| assignments | [assignments/00-overview.md](assignments/00-overview.md) |
| assessments | [assessments/00-overview.md](assessments/00-overview.md) |
| certificates | [certificates/00-overview.md](certificates/00-overview.md) |

<a id="verify"></a>
## Verify

```bash
curl -s http://localhost:8000/docs | head -c 200
```
Expected: HTML starting with `<!DOCTYPE html>` (FastAPI Swagger UI served).

# POST /api/auth/login — authenticate

> **Sources** — interview Q5; `Proposal/Documentation/project_documentation.md:621-637`; [data/users.md](../../data/users.md); [auth/00-overview.md](../../auth/00-overview.md)
> **Status** — [spec]
> **Page-size budget** — used 52 / 300 lines

<a id="purpose"></a>
## Purpose
Verifies `username` + `password` and returns a signed JWT carrying the user's role.

<a id="auth"></a>
## Auth
Public — no `Authorization` header required.

<a id="request"></a>
## Request

### Body
| Field | Type | Required | Constraints | Default |
|---|---|---|---|---|
| username | string | yes | non-empty; max 100 chars | — |
| password | string | yes | non-empty | — |

Schema source: `backend/app/schemas/user.py` `[planned]`

<a id="responses"></a>
## Responses

### 200 OK
```json
{
  "access_token": "<jwt>",
  "token_type": "bearer",
  "role": "ADMIN"
}
```

### 400 Bad Request
```json
{ "error": { "code": "MISSING_FIELDS", "message": "username and password are required" } }
```

### 401 Unauthorized
```json
{ "error": { "code": "INVALID_CREDENTIALS", "message": "invalid username or password" } }
```

<a id="side-effects"></a>
## Side effects
- Reads `users` by `username` → [data/users.md#read-patterns](../../data/users.md#read-patterns). No writes.

<a id="implementation"></a>
## Implementation
- Handler: `backend/app/routers/auth.py` `[planned]`
- Service: `backend/app/services/auth_service.py` `[planned]`
- JWT sign/verify helper: `backend/app/auth.py` `[planned]`

<a id="test-plan"></a>
## Test plan
| # | Case | Expected |
|---|---|---|
| 1 | `admin` / `admin123` | 200, `role` = `ADMIN`, token decodes with `sub` = admin id |
| 2 | `learner` / `learner123` | 200, `role` = `LEARNER` |
| 3 | wrong password | 401 `INVALID_CREDENTIALS` |
| 4 | empty body | 400 `MISSING_FIELDS` |

<a id="verify"></a>
## Verify

```bash
curl -s -X POST http://localhost:8000/api/auth/login -H "Content-Type: application/json" -d '{"username":"admin","password":"admin123"}'
```
Expected: JSON with `access_token` (3-part JWT), `token_type` = `bearer`, `role` = `ADMIN`.

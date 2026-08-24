# GET /api/certificates — list certificates

> **Sources** — `Proposal/Documentation/project_documentation.md:801-803`; [data/certificates.md](../../data/certificates.md); [auth/02-scopes.md](../../auth/02-scopes.md#certificates-read)
> **Status** — [spec]
> **Page-size budget** — used 42 / 300 lines

<a id="purpose"></a>
## Purpose
Returns certificates. Admin sees all; learner sees only their own.

<a id="auth"></a>
## Auth
- Required header: `Authorization: Bearer <jwt>`
- Required scope: `certificates:read` — [auth/02-scopes.md#certificates-read](../../auth/02-scopes.md#certificates-read)
- Scoping: for role `LEARNER`, filter by the caller's resolved `learner_id`.

<a id="request"></a>
## Request
No parameters.

<a id="responses"></a>
## Responses

### 200 OK
```json
[
  { "id": 1, "learner_id": 1, "course_id": 2, "certificate_number": "CERT-2026-001", "issued_date": "2026-08-24T10:00:00Z", "status": "CERTIFIED" }
]
```

### 401 Unauthorized
`MISSING_AUTH` | `INVALID_TOKEN`

### 403 Forbidden
`INSUFFICIENT_SCOPE`

<a id="side-effects"></a>
## Side effects
None.

<a id="implementation"></a>
## Implementation
- Handler: `backend/app/routers/certificates.py` `[planned]`

<a id="test-plan"></a>
## Test plan
| # | Case | Expected |
|---|---|---|
| 1 | ADMIN | 200, all certificates |
| 2 | LEARNER | 200, only own certificates |

<a id="verify"></a>
## Verify

```bash
curl -s http://localhost:8000/api/certificates -H "Authorization: Bearer $LEARNER_TOKEN"
```
Expected: HTTP 200; every item's `learner_id` equals the caller's learner id.

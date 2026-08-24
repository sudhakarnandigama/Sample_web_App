# GET /api/certificates/{id} — get certificate

> **Sources** — `Proposal/Documentation/project_documentation.md:805-807`; [data/certificates.md](../../data/certificates.md); [auth/02-scopes.md](../../auth/02-scopes.md#certificates-read)
> **Status** — [spec]
> **Page-size budget** — used 43 / 300 lines

<a id="purpose"></a>
## Purpose
Returns one certificate by id. Learner is restricted to own certificates.

<a id="auth"></a>
## Auth
- Required header: `Authorization: Bearer <jwt>`
- Required scope: `certificates:read` — [auth/02-scopes.md#certificates-read](../../auth/02-scopes.md#certificates-read)
- Ownership: role `LEARNER` may only read certificates whose `learner_id` equals their own.

<a id="request"></a>
## Request

### Path parameters
| Param | Type | Required |
|---|---|---|
| id | integer | yes |

<a id="responses"></a>
## Responses

### 200 OK
```json
{ "id": 1, "learner_id": 1, "course_id": 2, "certificate_number": "CERT-2026-001", "issued_date": "2026-08-24T10:00:00Z", "status": "CERTIFIED" }
```

### 404 Not Found
`CERTIFICATE_NOT_FOUND` — also returned when a `LEARNER` requests another learner's certificate (no existence leak).

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
| 1 | ADMIN, existing id | 200 |
| 2 | LEARNER, own certificate | 200 |
| 3 | LEARNER, other learner's certificate | 404 `CERTIFICATE_NOT_FOUND` |

<a id="verify"></a>
## Verify

```bash
curl -s http://localhost:8000/api/certificates/1 -H "Authorization: Bearer $ADMIN_TOKEN"
```
Expected: HTTP 200 with `certificate_number` matching `CERT-{YYYY}-{seq}`.

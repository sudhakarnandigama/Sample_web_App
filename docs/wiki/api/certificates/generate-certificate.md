# POST /api/certificates — generate certificate

> **Sources** — `Proposal/Documentation/project_documentation.md:309-338,813-817`; [data/certificates.md](../../data/certificates.md); [auth/02-scopes.md](../../auth/02-scopes.md#certificates-write)
> **Status** — [spec]
> **Page-size budget** — used 55 / 300 lines

<a id="purpose"></a>
## Purpose
Issues a certificate for a learner on a course, after verifying eligibility: the assignment is `COMPLETED` and the latest assessment attempt is `PASS`.

<a id="auth"></a>
## Auth
- Required header: `Authorization: Bearer <jwt>`
- Required scope: `certificates:write` — [auth/02-scopes.md#certificates-write](../../auth/02-scopes.md#certificates-write)
- Role `LEARNER`: `learner_id` is resolved from the JWT; the body's `learner_id` is ignored.

<a id="request"></a>
## Request

### Body
| Field | Type | Required | Constraints | Default |
|---|---|---|---|---|
| learner_id | integer | yes (admin) / ignored (learner) | references `learners.id` | — |
| course_id | integer | yes | references `courses.id` | — |

Schema source: `backend/app/schemas/certificate.py` `[planned]`

<a id="responses"></a>
## Responses

### 201 Created
```json
{ "id": 1, "learner_id": 1, "course_id": 2, "certificate_number": "CERT-2026-001", "issued_date": "2026-08-24T10:00:00Z", "status": "CERTIFIED" }
```

### 404 Not Found
`LEARNER_NOT_FOUND` | `COURSE_NOT_FOUND`

### 409 Conflict
- `CERTIFICATE_EXISTS` — certificate already issued for this learner+course.
- `NOT_ELIGIBLE` — assignment not `COMPLETED` or no `PASS` attempt.

### 401 Unauthorized
`MISSING_AUTH` | `INVALID_TOKEN`

### 403 Forbidden
`INSUFFICIENT_SCOPE`

<a id="side-effects"></a>
## Side effects
1. Insert into `certificates` → [data/certificates.md#write-patterns](../../data/certificates.md#write-patterns).
2. `certificate_number` is generated as `CERT-{YYYY}-{3-digit sequence}` — see [data/certificates.md#columns](../../data/certificates.md#columns).

<a id="implementation"></a>
## Implementation
- Handler: `backend/app/routers/certificates.py` `[planned]`
- Service: `backend/app/services/certificate_service.py` `[planned]`

<a id="test-plan"></a>
## Test plan
| # | Case | Expected |
|---|---|---|
| 1 | eligible learner | 201, unique `certificate_number` |
| 2 | not completed / not passed | 409 `NOT_ELIGIBLE` |
| 3 | already generated | 409 `CERTIFICATE_EXISTS` |

<a id="verify"></a>
## Verify

```bash
curl -s -X POST http://localhost:8000/api/certificates -H "Authorization: Bearer $LEARNER_TOKEN" -H "Content-Type: application/json" -d '{"course_id":2}'
```
Expected: HTTP 201 with `certificate_number` = `CERT-{YYYY}-{seq}`, or 409 `NOT_ELIGIBLE`/`CERTIFICATE_EXISTS`.

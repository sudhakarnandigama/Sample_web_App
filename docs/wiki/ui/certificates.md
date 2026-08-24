# Route: /certificates — Certificates

> **Sources** — `Proposal/Documentation/project_documentation.md:309-338`; [api/certificates/list-certificates.md](../api/certificates/list-certificates.md)
> **Status** — [spec]
> **Page-size budget** — used 36 / 300 lines

<a id="purpose"></a>
## Purpose
Lists certificates — all for admin, own for learner.

<a id="route"></a>
## Route
- Path: `/certificates`
- File: `frontend/src/app/features/certificates/certificates.component.ts` `[planned]`
- Auth required: yes (`certificates:read`)

<a id="state"></a>
## Local state
| Name | Type | Initial | Updated by |
|---|---|---|---|
| certificates | array | [] | GET `/api/certificates` response |

<a id="behavior"></a>
## Behavior
1. On init: GET `/api/certificates` per [api/certificates/list-certificates.md](../api/certificates/list-certificates.md).
2. Render `certificate_number`, learner, course, `issued_date`, `status`.
3. Click a row → GET `/api/certificates/{id}` per [api/certificates/get-certificate.md](../api/certificates/get-certificate.md) for the detail view.

<a id="components"></a>
## Components used
- `<DataTable>`, `<StatusBadge>` — `frontend/src/app/shared/**` `[planned]`

<a id="test-plan"></a>
## Test plan
| # | Case | Expected |
|---|---|---|
| 1 | admin opens /certificates | all certificates |
| 2 | learner opens /certificates | only own certificates |

<a id="verify"></a>
## Verify

```bash
curl -s http://localhost:8000/api/certificates -H "Authorization: Bearer $TOKEN"
```
Expected: HTTP 200, JSON array rendered by the page.

# Resource: certificates

> **Sources** — interview Q2; `Proposal/Documentation/project_documentation.md:309-338,799-817`
> **Status** — [spec]
> **Page-size budget** — used 26 / 200 lines

Issued certificates. Schema: [data/certificates.md](../../data/certificates.md).

| Method | Path | Endpoint page | Scope |
|---|---|---|---|
| GET | `/api/certificates` | [list-certificates.md](list-certificates.md) | `certificates:read` |
| GET | `/api/certificates/{id}` | [get-certificate.md](get-certificate.md) | `certificates:read` |
| POST | `/api/certificates` | [generate-certificate.md](generate-certificate.md) | `certificates:write` |

Certificate object: `{ "id", "learner_id", "course_id", "certificate_number", "issued_date", "status" }` — see [data/certificates.md#columns](../../data/certificates.md#columns).

<a id="verify"></a>
## Verify

```bash
curl -s http://localhost:8000/api/certificates -H "Authorization: Bearer $ADMIN_TOKEN"
```
Expected: HTTP 200, JSON array.

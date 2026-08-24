# Route: /assessment/result — Assessment result

> **Sources** — `Proposal/Documentation/project_documentation.md:300-305`; [api/assessments/submit-assessment.md](../api/assessments/submit-assessment.md); [api/certificates/generate-certificate.md](../api/certificates/generate-certificate.md)
> **Status** — [spec]
> **Page-size budget** — used 38 / 300 lines

<a id="purpose"></a>
## Purpose
Shows the score and pass/fail result; on pass, offers certificate generation.

<a id="route"></a>
## Route
- Path: `/assessment/result`
- File: `frontend/src/app/features/assessments/assessment-result.component.ts` `[planned]`
- Auth required: yes (`certificates:write` for the generate action)

<a id="state"></a>
## Local state
| Name | Type | Initial | Updated by |
|---|---|---|---|
| score | number \| null | null | route data from submit |
| result | string \| null | null | route data from submit |
| certError | string \| null | null | generate-certificate error |

<a id="behavior"></a>
## Behavior
1. Display `score` + `result` passed from [assessment.md](assessment.md).
2. If `PASS`: show "Generate certificate" → POST `/api/certificates` per [api/certificates/generate-certificate.md](../api/certificates/generate-certificate.md).
3. On 201: navigate `/certificates`.
4. On 409 `NOT_ELIGIBLE`: "Complete the course first". On 409 `CERTIFICATE_EXISTS`: "Certificate already generated".

<a id="components"></a>
## Components used
- `<ResultCard>`, `<Button>` — `frontend/src/app/shared/**` `[planned]`

<a id="test-plan"></a>
## Test plan
| # | Case | Expected |
|---|---|---|
| 1 | PASS result | score + PASS shown, generate button visible |
| 2 | FAIL result | score + FAIL shown, no generate button |

<a id="verify"></a>
## Verify

```bash
curl -s -X POST http://localhost:8000/api/assessments/1/submit -H "Authorization: Bearer $LEARNER_TOKEN" -H "Content-Type: application/json" -d '{"answers":{}}'
```
Expected: HTTP 200 with `score` + `result`, or 400 `INVALID_SUBMISSION`.

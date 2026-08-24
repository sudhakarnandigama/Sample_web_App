# POST /api/assessments/{id}/submit — submit assessment

> **Sources** — `Proposal/Documentation/project_documentation.md:769-795`; [data/assessment_attempts.md](../../data/assessment_attempts.md); [auth/02-scopes.md](../../auth/02-scopes.md#assessments-submit)
> **Status** — [spec]
> **Page-size budget** — used 52 / 300 lines

<a id="purpose"></a>
## Purpose
Scores the learner's answers and records the attempt. The `learner_id` is resolved from the JWT, not trusted from the body.

<a id="auth"></a>
## Auth
- Required header: `Authorization: Bearer <jwt>`
- Required scope: `assessments:submit` — [auth/02-scopes.md#assessments-submit](../../auth/02-scopes.md#assessments-submit)

<a id="request"></a>
## Request

### Path parameters
| Param | Type | Required |
|---|---|---|
| id | integer | yes |

### Body
| Field | Type | Required | Constraints | Default |
|---|---|---|---|---|
| answers | object | yes | map of question id → `A`\|`B`\|`C`\|`D` | — |

```json
{ "answers": { "1": "A", "2": "C", "3": "B" } }
```
PRD §23 example also shows `learner_id` in the body; the spec resolves it server-side from the JWT to prevent spoofing.

<a id="responses"></a>
## Responses

### 200 OK
```json
{ "score": 80, "result": "PASS" }
```
`result` = `PASS` iff `score >= assessments.passing_score`.

### 400 Bad Request
`INVALID_SUBMISSION` — `answers` missing, a question id does not belong to this assessment, or an answer value is not `A`–`D`.

### 404 Not Found
`ASSESSMENT_NOT_FOUND`

### 401 Unauthorized
`MISSING_AUTH` | `INVALID_TOKEN`

### 403 Forbidden
`INSUFFICIENT_SCOPE`

<a id="side-effects"></a>
## Side effects
1. Insert into `assessment_attempts` → [data/assessment_attempts.md#write-patterns](../../data/assessment_attempts.md#write-patterns).
2. Certificate is NOT auto-created here; the UI calls [generate-certificate.md](../certificates/generate-certificate.md) after a `PASS`.

<a id="implementation"></a>
## Implementation
- Handler: `backend/app/routers/assessments.py` `[planned]`
- Service: `backend/app/services/assessment_service.py` `[planned]`

<a id="test-plan"></a>
## Test plan
| # | Case | Expected |
|---|---|---|
| 1 | all correct | 200, `score` = 100, `result` = `PASS` |
| 2 | below passing_score | 200, `result` = `FAIL` |
| 3 | unknown question id | 400 `INVALID_SUBMISSION` |

<a id="verify"></a>
## Verify

```bash
curl -s -X POST http://localhost:8000/api/assessments/1/submit -H "Authorization: Bearer $LEARNER_TOKEN" -H "Content-Type: application/json" -d '{"answers":{"1":"A","2":"C","3":"B"}}'
```
Expected: HTTP 200 with `score` (integer 0–100) and `result` (`PASS` or `FAIL`).

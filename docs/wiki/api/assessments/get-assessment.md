# GET /api/assessments/{course_id} — get assessment

> **Sources** — `Proposal/Documentation/project_documentation.md:763-767`; [data/assessments.md](../../data/assessments.md); [data/questions.md](../../data/questions.md); [auth/02-scopes.md](../../auth/02-scopes.md#assessments-read)
> **Status** — [spec]
> **Page-size budget** — used 45 / 300 lines

<a id="purpose"></a>
## Purpose
Returns a course's assessment and its questions for the learner to take. `correct_option` is omitted from the response.

<a id="auth"></a>
## Auth
- Required header: `Authorization: Bearer <jwt>`
- Required scope: `assessments:read` — [auth/02-scopes.md#assessments-read](../../auth/02-scopes.md#assessments-read)

<a id="request"></a>
## Request

### Path parameters
| Param | Type | Required |
|---|---|---|
| course_id | integer | yes |

<a id="responses"></a>
## Responses

### 200 OK
```json
{
  "id": 1,
  "course_id": 2,
  "title": "Python Fundamentals Quiz",
  "passing_score": 60,
  "questions": [
    { "id": 1, "question_text": "Which language is commonly used with FastAPI?", "option_a": "Python", "option_b": "Java", "option_c": "C#", "option_d": "PHP" }
  ]
}
```

### 404 Not Found
`ASSESSMENT_NOT_FOUND` — no assessment for this course.

### 401 Unauthorized
`MISSING_AUTH` | `INVALID_TOKEN`

### 403 Forbidden
`INSUFFICIENT_SCOPE`

<a id="side-effects"></a>
## Side effects
None.

<a id="implementation"></a>
## Implementation
- Handler: `backend/app/routers/assessments.py` `[planned]`

<a id="test-plan"></a>
## Test plan
| # | Case | Expected |
|---|---|---|
| 1 | course with assessment | 200; no `correct_option` key in any question |
| 2 | course without assessment | 404 `ASSESSMENT_NOT_FOUND` |

<a id="verify"></a>
## Verify

```bash
curl -s http://localhost:8000/api/assessments/2 -H "Authorization: Bearer $LEARNER_TOKEN"
```
Expected: HTTP 200; `questions` array present; no `correct_option` in questions.

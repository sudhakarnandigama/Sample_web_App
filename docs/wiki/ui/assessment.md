# Route: /assessment/:courseId — Take assessment

> **Sources** — `Proposal/Documentation/project_documentation.md:277-306`; [api/assessments/get-assessment.md](../api/assessments/get-assessment.md); [api/assessments/submit-assessment.md](../api/assessments/submit-assessment.md)
> **Status** — [spec]
> **Page-size budget** — used 40 / 300 lines

<a id="purpose"></a>
## Purpose
Learner answers the course's multiple-choice questions and submits.

<a id="route"></a>
## Route
- Path: `/assessment/:courseId`
- File: `frontend/src/app/features/assessments/assessment.component.ts` `[planned]`
- Auth required: yes (`assessments:read` + `assessments:submit`)

<a id="state"></a>
## Local state
| Name | Type | Initial | Updated by |
|---|---|---|---|
| assessment | object \| null | null | GET response |
| answers | object | {} | option selection |
| isSubmitting | boolean | false | submit start/end |

<a id="behavior"></a>
## Behavior
1. On init: GET `/api/assessments/{courseId}` per [api/assessments/get-assessment.md](../api/assessments/get-assessment.md).
2. Learner selects one option per question → `answers[question_id] = 'A'|'B'|'C'|'D'`.
3. Submit → POST `/api/assessments/{id}/submit` per [api/assessments/submit-assessment.md](../api/assessments/submit-assessment.md).
4. On 200: navigate `/assessment/result` with score/result.
5. On 404 `ASSESSMENT_NOT_FOUND`: "No assessment for this course".

<a id="components"></a>
## Components used
- `<QuestionCard>`, `<RadioGroup>`, `<Button>` — `frontend/src/app/shared/**` `[planned]`

<a id="test-plan"></a>
## Test plan
| # | Case | Expected |
|---|---|---|
| 1 | all questions answered, submit | navigate to result |
| 2 | unanswered question | inline "answer all questions" |

<a id="verify"></a>
## Verify

```bash
curl -s http://localhost:8000/api/assessments/2 -H "Authorization: Bearer $LEARNER_TOKEN"
```
Expected: HTTP 200, `questions` array rendered by the page.

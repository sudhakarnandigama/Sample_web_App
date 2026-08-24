# Resource: assessments

> **Sources** — interview Q2; `Proposal/Documentation/project_documentation.md:277-306,761-795`
> **Status** — [spec]
> **Page-size budget** — used 25 / 200 lines

Multiple-choice assessments. Schema: [data/assessments.md](../../data/assessments.md), [data/questions.md](../../data/questions.md).

| Method | Path | Endpoint page | Scope |
|---|---|---|---|
| GET | `/api/assessments/{course_id}` | [get-assessment.md](get-assessment.md) | `assessments:read` |
| POST | `/api/assessments/{id}/submit` | [submit-assessment.md](submit-assessment.md) | `assessments:submit` |

Assessment/question creation is seeded only — no CRUD endpoint exists in PRD §18–24 (`[GAP-ASMT-01]`). See [data/assessments.md#write-patterns](../../data/assessments.md#write-patterns).

<a id="verify"></a>
## Verify

```bash
curl -s http://localhost:8000/api/assessments/2 -H "Authorization: Bearer $LEARNER_TOKEN"
```
Expected: HTTP 200, JSON with `questions` array.

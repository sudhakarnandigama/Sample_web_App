# Test fixtures — canonical seed data

> **Sources** — `Proposal/Documentation/project_documentation.md:821-877`; `docs/sources/decisions/2026-08-24-auth-transport.md`
> **Status** — [spec]
> **Page-size budget** — used 44 / 300 lines

Canonical seed data loaded by `backend/seed.py` `[planned]` (see [ops/runbooks/seed-data.md](../ops/runbooks/seed-data.md)).

<a id="users"></a>
## users
| id | username | password (seed input) | stored as | role | full_name |
|---|---|---|---|---|---|
| 1 | admin | admin123 | `pbkdf2_sha256$<salt>$<hash>` | ADMIN | Admin User |
| 2 | learner | learner123 | `pbkdf2_sha256$<salt>$<hash>` | LEARNER | Learner User |

Passwords are hashed at seed time per [auth-transport ADR](../../sources/decisions/2026-08-24-auth-transport.md).

<a id="courses"></a>
## courses
| id | title | description | duration_hours | status |
|---|---|---|---|---|
| 1 | Java Full Stack Development | Java + Spring + Angular | 40 | ACTIVE |
| 2 | Python Fundamentals | Python + FastAPI basics | 8 | ACTIVE |
| 3 | Web Development Basics | HTML/CSS/JS | 12 | ACTIVE |

<a id="learners"></a>
## learners
| id | user_id | name | email | department | status |
|---|---|---|---|---|---|
| 1 | 2 | John Doe | john@example.com | IT | ACTIVE |
| 2 | NULL | Priya Sharma | priya@example.com | HR | ACTIVE |
| 3 | NULL | Rahul Kumar | rahul@example.com | IT | ACTIVE |
| 4 | NULL | Anjali Rao | anjali@example.com | HR | ACTIVE |
| 5 | NULL | David Smith | david@example.com | IT | ACTIVE |

Learner id 1 is linked to user id 2 per [learner-user-link ADR](../../sources/decisions/2026-08-24-learner-user-link.md).

<a id="assessment"></a>
## assessments + questions (course 2)
| id | course_id | title | passing_score |
|---|---|---|---|
| 1 | 2 | Python Fundamentals Quiz | 60 |

| id | assessment_id | question_text | option_a..d | correct_option |
|---|---|---|---|---|
| 1 | 1 | Which language is commonly used with FastAPI? | Python / Java / C# / PHP | A |

<a id="certificate-format"></a>
## certificate_number
`CERT-{YYYY}-{3-digit sequence}` — first issued: `CERT-2026-001` (`Proposal/Documentation/project_documentation.md:331`).

<a id="verify"></a>
## Verify

```bash
python -c "import sqlite3; c=sqlite3.connect('backend/training_demo.db'); print(c.execute('SELECT count(*) FROM learners').fetchone()[0])"
```
Expected: `5` (seeded learners).

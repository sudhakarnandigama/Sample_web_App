# Bootstrap interview — 2026-08-24

Verbatim answers from Phase 1 of the Spec Bootstrap workflow. This file is the canonical Source for every wiki page that cites `interview Q<N>`. Append-only after creation.

Answers were derived from the project PRD at `Proposal/Documentation/project_documentation.md` (Q10 spec input) and confirmed by the user on 2026-08-24.

## Q1 — PROJECT_NAME
employee-training-demo

## Q2 — ONE_LINE_PURPOSE
Employee Training & Certification Demo System is a demo web application that lets an administrator manage courses and learners, and lets learners track course progress, take assessments, and earn certificates.

## Q3 — ARCHITECTURE
monolith

## Q4 — PRIMARY_STACK
Angular + Python FastAPI + SQLite 3 + SQLAlchemy

## Q5 — AUTH_MODEL
JWT bearer with a role claim (`ADMIN` | `LEARNER`). Simple username/password login. Confirmed by user on 2026-08-24. The PRD §3 and §5.1 specified only "simple demo authentication"; OAuth is explicitly excluded in §42.

## Q6 — DATABASE / ORM
SQLite / SQLAlchemy

## Q7 — DEPLOYABLE_UNITS
frontend, backend

## Q8 — ROADMAP_PHASES
none — single phase demo

## Q9 — EXTERNAL_READERS
coding-agent development and testing

## Q10 — SPEC_INPUT
Proposal/Documentation/project_documentation.md

## Scope contract (confirmed 2026-08-24)
1. Project: employee-training-demo
2. Purpose: Employee Training & Certification Demo System is a demo web application that lets an admin manage courses/learners and lets learners track progress, take assessments, and earn certificates
3. Architecture: monolith (Angular frontend + FastAPI backend, single local deploy)
4. Stack: Angular + FastAPI + SQLite 3 + SQLAlchemy
5. Auth: JWT bearer with a role claim (`ADMIN` | `LEARNER`), simple username/password login
6. DB / ORM: SQLite / SQLAlchemy
7. Deployables: frontend, backend
8. Phases: none — single phase demo
9. External readers: coding-agent development and testing
10. Spec input: Proposal/Documentation/project_documentation.md

## External URL allowlist
External URLs cited anywhere in the wiki must appear here. Add entries as the user supplies them; the audit script rejects any wiki link to a URL not in this list.

- (none — no external URLs are cited in the wiki)

"""Seed the SQLite database with the canonical demo data.

Run from the repository root: ``python backend/seed.py``.

Canonical data: docs/wiki/test/fixtures.md
"""

import os

# The seed hashes passwords only; JWT_SECRET is not needed for hashing but
# config.py fails fast if it is unset.
os.environ.setdefault("JWT_SECRET", "demo-secret-change-me")

from sqlalchemy.orm import Session

from app.auth import hash_password
from app.database import Base, SessionLocal, engine
from app.models import Assessment, Course, Learner, Question, User


def reset() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def seed(db: Session) -> None:
    admin = User(
        username="admin",
        password_hash=hash_password("admin123"),
        role="ADMIN",
        full_name="Admin User",
    )
    learner_user = User(
        username="learner",
        password_hash=hash_password("learner123"),
        role="LEARNER",
        full_name="Learner User",
    )
    db.add_all([admin, learner_user])
    db.flush()

    courses = [
        Course(
            title="Java Full Stack Development",
            description="Java + Spring + Angular",
            duration_hours=40,
            status="ACTIVE",
        ),
        Course(
            title="Python Fundamentals",
            description="Python + FastAPI basics",
            duration_hours=8,
            status="ACTIVE",
        ),
        Course(
            title="Web Development Basics",
            description="HTML/CSS/JS",
            duration_hours=12,
            status="ACTIVE",
        ),
    ]
    db.add_all(courses)
    db.flush()

    learners = [
        Learner(
            user_id=learner_user.id,
            name="John Doe",
            email="john@example.com",
            department="IT",
            status="ACTIVE",
        ),
        Learner(
            user_id=None,
            name="Priya Sharma",
            email="priya@example.com",
            department="HR",
            status="ACTIVE",
        ),
        Learner(
            user_id=None,
            name="Rahul Kumar",
            email="rahul@example.com",
            department="IT",
            status="ACTIVE",
        ),
        Learner(
            user_id=None,
            name="Anjali Rao",
            email="anjali@example.com",
            department="HR",
            status="ACTIVE",
        ),
        Learner(
            user_id=None,
            name="David Smith",
            email="david@example.com",
            department="IT",
            status="ACTIVE",
        ),
    ]
    db.add_all(learners)
    db.flush()

    assessment = Assessment(
        course_id=courses[1].id,
        title="Python Fundamentals Quiz",
        passing_score=60,
    )
    db.add(assessment)
    db.flush()

    question = Question(
        assessment_id=assessment.id,
        question_text="Which language is commonly used with FastAPI?",
        option_a="Python",
        option_b="Java",
        option_c="C#",
        option_d="PHP",
        correct_option="A",
    )
    db.add(question)

    db.commit()


if __name__ == "__main__":
    reset()
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()
    print("Seed complete.")
    print(f"  users: {db.query(User).count()}")
    print(f"  courses: {db.query(Course).count()}")
    print(f"  learners: {db.query(Learner).count()}")
    print(f"  assessments: {db.query(Assessment).count()}")
    print(f"  questions: {db.query(Question).count()}")

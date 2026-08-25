import os

os.environ["JWT_SECRET"] = "test-secret-that-is-longer-than-32-bytes"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.auth import hash_password
from app.database import Base, get_db
from app.main import app
from app.models import Assessment, Course, Learner, Question, User


def seed_canonical(db):
    """Insert the canonical demo fixture (docs/wiki/test/fixtures.md)."""
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
        Course(title="Java Full Stack Development", description="Java + Spring + Angular", duration_hours=40, status="ACTIVE"),
        Course(title="Python Fundamentals", description="Python + FastAPI basics", duration_hours=8, status="ACTIVE"),
        Course(title="Web Development Basics", description="HTML/CSS/JS", duration_hours=12, status="ACTIVE"),
    ]
    db.add_all(courses)
    db.flush()

    learners = [
        Learner(user_id=learner_user.id, name="John Doe", email="john@example.com", department="IT", status="ACTIVE"),
        Learner(user_id=None, name="Priya Sharma", email="priya@example.com", department="HR", status="ACTIVE"),
        Learner(user_id=None, name="Rahul Kumar", email="rahul@example.com", department="IT", status="ACTIVE"),
        Learner(user_id=None, name="Anjali Rao", email="anjali@example.com", department="HR", status="ACTIVE"),
        Learner(user_id=None, name="David Smith", email="david@example.com", department="IT", status="ACTIVE"),
    ]
    db.add_all(learners)
    db.flush()

    assessment = Assessment(course_id=courses[1].id, title="Python Fundamentals Quiz", passing_score=60)
    db.add(assessment)
    db.flush()

    db.add(
        Question(
            assessment_id=assessment.id,
            question_text="Which language is commonly used with FastAPI?",
            option_a="Python",
            option_b="Java",
            option_c="C#",
            option_d="PHP",
            correct_option="A",
        )
    )
    db.commit()


@pytest.fixture()
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    @event.listens_for(engine, "connect")
    def _fk_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine, autocommit=False, autoflush=False)()
    seed_canonical(session)
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def admin_token(client):
    resp = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    return resp.json()["access_token"]


@pytest.fixture()
def learner_token(client):
    resp = client.post("/api/auth/login", json={"username": "learner", "password": "learner123"})
    return resp.json()["access_token"]


def auth(token):
    return {"Authorization": f"Bearer {token}"}

from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, String, UniqueConstraint

from ..database import Base


def _utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class Assessment(Base):
    __tablename__ = "assessments"
    __table_args__ = (
        CheckConstraint("passing_score BETWEEN 0 AND 100", name="ck_assessments_passing"),
        UniqueConstraint("course_id", name="uq_assessments_course"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    passing_score = Column(Integer, nullable=False, default=60)


class Question(Base):
    __tablename__ = "questions"
    __table_args__ = (
        CheckConstraint("correct_option IN ('A','B','C','D')", name="ck_questions_correct"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    assessment_id = Column(
        Integer, ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False
    )
    question_text = Column(String, nullable=False)
    option_a = Column(String, nullable=False)
    option_b = Column(String, nullable=False)
    option_c = Column(String, nullable=False)
    option_d = Column(String, nullable=False)
    correct_option = Column(String, nullable=False)


class AssessmentAttempt(Base):
    __tablename__ = "assessment_attempts"
    __table_args__ = (
        CheckConstraint("score BETWEEN 0 AND 100", name="ck_attempts_score"),
        CheckConstraint("result IN ('PASS','FAIL')", name="ck_attempts_result"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    assessment_id = Column(
        Integer, ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False
    )
    learner_id = Column(Integer, ForeignKey("learners.id", ondelete="CASCADE"), nullable=False)
    score = Column(Integer, nullable=False)
    result = Column(String, nullable=False)
    attempted_at = Column(String, nullable=False, default=_utcnow)

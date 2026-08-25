from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, String, UniqueConstraint

from ..database import Base


def _utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class Assignment(Base):
    __tablename__ = "course_assignments"
    __table_args__ = (
        CheckConstraint("progress BETWEEN 0 AND 100", name="ck_assignments_progress"),
        CheckConstraint(
            "status IN ('NOT_STARTED','IN_PROGRESS','COMPLETED')",
            name="ck_assignments_status",
        ),
        UniqueConstraint("course_id", "learner_id", name="uq_assignments_course_learner"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    learner_id = Column(Integer, ForeignKey("learners.id", ondelete="CASCADE"), nullable=False)
    progress = Column(Integer, nullable=False, default=0)
    status = Column(String, nullable=False, default="NOT_STARTED")
    assigned_date = Column(String, nullable=False, default=_utcnow)

from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, Column, Integer, String

from ..database import Base


def _utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class Course(Base):
    __tablename__ = "courses"
    __table_args__ = (
        CheckConstraint("duration_hours > 0", name="ck_courses_duration"),
        CheckConstraint("status IN ('ACTIVE','INACTIVE')", name="ck_courses_status"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    duration_hours = Column(Integer, nullable=False)
    status = Column(String, nullable=False, default="ACTIVE")
    created_at = Column(String, nullable=False, default=_utcnow)

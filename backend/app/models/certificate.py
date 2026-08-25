from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, String, UniqueConstraint

from ..database import Base


def _utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class Certificate(Base):
    __tablename__ = "certificates"
    __table_args__ = (
        CheckConstraint("status IN ('CERTIFIED')", name="ck_certificates_status"),
        UniqueConstraint("learner_id", "course_id", name="uq_certificates_learner_course"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    learner_id = Column(Integer, ForeignKey("learners.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    certificate_number = Column(String, nullable=False, unique=True)
    issued_date = Column(String, nullable=False, default=_utcnow)
    status = Column(String, nullable=False, default="CERTIFIED")

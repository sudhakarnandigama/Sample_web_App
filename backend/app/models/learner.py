from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, String

from ..database import Base


def _utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class Learner(Base):
    __tablename__ = "learners"
    __table_args__ = (
        CheckConstraint("status IN ('ACTIVE','INACTIVE')", name="ck_learners_status"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), unique=True, nullable=True
    )
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    department = Column(String, nullable=False)
    status = Column(String, nullable=False, default="ACTIVE")
    created_at = Column(String, nullable=False, default=_utcnow)

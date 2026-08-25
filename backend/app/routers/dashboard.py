from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..auth import CurrentUser, require_scope
from ..database import get_db
from ..models import Assignment, Certificate, Course, Learner

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("")
def get_dashboard(
    current: CurrentUser = Depends(require_scope("dashboard:read")),
    db: Session = Depends(get_db),
):
    if current.role == "ADMIN":
        return {
            "total_learners": db.query(func.count(Learner.id)).scalar(),
            "total_courses": db.query(func.count(Course.id)).scalar(),
            "active_courses": db.query(func.count(Course.id))
            .filter(Course.status == "ACTIVE")
            .scalar(),
            "completed_courses": db.query(func.count(Assignment.id))
            .filter(Assignment.status == "COMPLETED")
            .scalar(),
            "certificates": db.query(func.count(Certificate.id)).scalar(),
        }

    learner_id = current.learner_id
    return {
        "assigned_courses": db.query(func.count(Assignment.id))
        .filter(Assignment.learner_id == learner_id)
        .scalar(),
        "in_progress": db.query(func.count(Assignment.id))
        .filter(Assignment.learner_id == learner_id, Assignment.status == "IN_PROGRESS")
        .scalar(),
        "completed": db.query(func.count(Assignment.id))
        .filter(Assignment.learner_id == learner_id, Assignment.status == "COMPLETED")
        .scalar(),
        "certificates": db.query(func.count(Certificate.id))
        .filter(Certificate.learner_id == learner_id)
        .scalar(),
    }

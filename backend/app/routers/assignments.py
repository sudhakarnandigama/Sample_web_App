from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..auth import CurrentUser, require_scope
from ..database import get_db
from ..errors import ApiError
from ..models import Assignment, Course, Learner
from ..schemas.assignment import AssignmentCreate, ProgressUpdate

router = APIRouter(prefix="/assignments", tags=["assignments"])


def derive_status(progress: int) -> str:
    if progress == 100:
        return "COMPLETED"
    if progress > 0:
        return "IN_PROGRESS"
    return "NOT_STARTED"


def assignment_out(assignment: Assignment, learner_name: str = None, course_title: str = None) -> dict:
    data = {
        "id": assignment.id,
        "course_id": assignment.course_id,
        "learner_id": assignment.learner_id,
        "progress": assignment.progress,
        "status": assignment.status,
        "assigned_date": assignment.assigned_date,
    }
    if learner_name is not None:
        data["learner_name"] = learner_name
    if course_title is not None:
        data["course_title"] = course_title
    return data


@router.get("")
def list_assignments(
    current: CurrentUser = Depends(require_scope("assignments:write")),
    db: Session = Depends(get_db),
):
    rows = (
        db.query(Assignment, Learner.name, Course.title)
        .join(Learner, Assignment.learner_id == Learner.id)
        .join(Course, Assignment.course_id == Course.id)
        .order_by(Assignment.id)
        .all()
    )
    return [assignment_out(a, learner_name=ln, course_title=ct) for a, ln, ct in rows]


@router.post("", status_code=201)
def create_assignment(
    body: AssignmentCreate,
    current: CurrentUser = Depends(require_scope("assignments:write")),
    db: Session = Depends(get_db),
):
    if db.get(Learner, body.learner_id) is None:
        raise ApiError("LEARNER_NOT_FOUND", f"no learner with id {body.learner_id}", 404)
    if db.get(Course, body.course_id) is None:
        raise ApiError("COURSE_NOT_FOUND", f"no course with id {body.course_id}", 404)

    existing = (
        db.query(Assignment)
        .filter(Assignment.course_id == body.course_id, Assignment.learner_id == body.learner_id)
        .first()
    )
    if existing is not None:
        raise ApiError("ASSIGNMENT_EXISTS", "course already assigned to this learner", 409)

    assignment = Assignment(
        course_id=body.course_id,
        learner_id=body.learner_id,
        progress=0,
        status="NOT_STARTED",
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment_out(assignment)


@router.put("/{assignment_id}/progress")
def update_progress(
    assignment_id: int,
    body: ProgressUpdate,
    current: CurrentUser = Depends(require_scope("progress:write:own")),
    db: Session = Depends(get_db),
):
    assignment = db.get(Assignment, assignment_id)
    if assignment is None:
        raise ApiError("ASSIGNMENT_NOT_FOUND", f"no assignment with id {assignment_id}", 404)

    if current.learner_id is None or assignment.learner_id != current.learner_id:
        raise ApiError("INSUFFICIENT_SCOPE", "you can only update your own assignments", 403)

    if body.progress < 0 or body.progress > 100:
        raise ApiError("INVALID_PROGRESS", "progress must be between 0 and 100", 400)

    status = body.status
    if status is not None:
        status = status.strip().upper()
        if status not in ("NOT_STARTED", "IN_PROGRESS", "COMPLETED"):
            raise ApiError("INVALID_PROGRESS", "invalid status value", 400)
        expected = derive_status(body.progress)
        if status != expected:
            raise ApiError("INVALID_PROGRESS", "status is inconsistent with progress", 400)
    else:
        status = derive_status(body.progress)

    assignment.progress = body.progress
    assignment.status = status
    db.commit()
    db.refresh(assignment)
    return assignment_out(assignment)

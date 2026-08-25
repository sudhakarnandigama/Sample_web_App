import re

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from ..auth import require_scope
from ..database import get_db
from ..errors import ApiError
from ..models import Learner
from ..schemas.learner import LearnerCreate, LearnerUpdate

router = APIRouter(prefix="/learners", tags=["learners"])

EMAIL_RE = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")


def learner_out(learner: Learner) -> dict:
    return {
        "id": learner.id,
        "user_id": learner.user_id,
        "name": learner.name,
        "email": learner.email,
        "department": learner.department,
        "status": learner.status,
        "created_at": learner.created_at,
    }


def _clean_name(name: str) -> str:
    name = (name or "").strip()
    if not name or len(name) > 100:
        raise ApiError("INVALID_LEARNER", "name is required and at most 100 characters", 400)
    return name


def _clean_email(email: str) -> str:
    email = (email or "").strip()
    if not email or len(email) > 254 or not EMAIL_RE.fullmatch(email):
        raise ApiError("INVALID_LEARNER", "a valid email address is required", 400)
    return email


def _clean_department(department: str) -> str:
    department = (department or "").strip()
    if not department or len(department) > 100:
        raise ApiError("INVALID_LEARNER", "department is required and at most 100 characters", 400)
    return department


def _ensure_email_available(db: Session, email: str, exclude_id: int | None = None) -> None:
    query = db.query(Learner).filter(Learner.email == email)
    if exclude_id is not None:
        query = query.filter(Learner.id != exclude_id)
    if query.first() is not None:
        raise ApiError("EMAIL_EXISTS", "a learner with this email already exists", 409)


@router.get("")
def list_learners(
    current=Depends(require_scope("learners:read")),
    db: Session = Depends(get_db),
):
    return [learner_out(l) for l in db.query(Learner).order_by(Learner.id).all()]


@router.get("/{learner_id}")
def get_learner(
    learner_id: int,
    current=Depends(require_scope("learners:read")),
    db: Session = Depends(get_db),
):
    learner = db.get(Learner, learner_id)
    if learner is None:
        raise ApiError("LEARNER_NOT_FOUND", f"no learner with id {learner_id}", 404)
    return learner_out(learner)


@router.post("", status_code=201)
def create_learner(
    body: LearnerCreate,
    current=Depends(require_scope("learners:write")),
    db: Session = Depends(get_db),
):
    email = _clean_email(body.email)
    _ensure_email_available(db, email)
    learner = Learner(
        name=_clean_name(body.name),
        email=email,
        department=_clean_department(body.department),
        status="ACTIVE",
    )
    db.add(learner)
    db.commit()
    db.refresh(learner)
    return learner_out(learner)


@router.put("/{learner_id}")
def update_learner(
    learner_id: int,
    body: LearnerUpdate,
    current=Depends(require_scope("learners:write")),
    db: Session = Depends(get_db),
):
    learner = db.get(Learner, learner_id)
    if learner is None:
        raise ApiError("LEARNER_NOT_FOUND", f"no learner with id {learner_id}", 404)

    if body.name is not None:
        learner.name = _clean_name(body.name)
    if body.email is not None:
        email = _clean_email(body.email)
        _ensure_email_available(db, email, exclude_id=learner.id)
        learner.email = email
    if body.department is not None:
        learner.department = _clean_department(body.department)
    if body.status is not None:
        status = body.status.strip().upper()
        if status not in ("ACTIVE", "INACTIVE"):
            raise ApiError("INVALID_LEARNER", "status must be ACTIVE or INACTIVE", 400)
        learner.status = status

    db.commit()
    db.refresh(learner)
    return learner_out(learner)


@router.delete("/{learner_id}", status_code=204)
def delete_learner(
    learner_id: int,
    current=Depends(require_scope("learners:write")),
    db: Session = Depends(get_db),
):
    learner = db.get(Learner, learner_id)
    if learner is None:
        raise ApiError("LEARNER_NOT_FOUND", f"no learner with id {learner_id}", 404)
    db.delete(learner)
    db.commit()
    return Response(status_code=204)

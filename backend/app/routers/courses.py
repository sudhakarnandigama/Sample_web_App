from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from ..auth import require_scope
from ..database import get_db
from ..errors import ApiError
from ..models import Course
from ..schemas.course import CourseCreate, CourseUpdate

router = APIRouter(prefix="/courses", tags=["courses"])


def course_out(course: Course) -> dict:
    return {
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "duration_hours": course.duration_hours,
        "status": course.status,
        "created_at": course.created_at,
    }


def _clean_title(title: str) -> str:
    title = (title or "").strip()
    if not title or len(title) > 200:
        raise ApiError("INVALID_COURSE", "title is required and at most 200 characters", 400)
    return title


def _clean_description(description: str) -> str:
    description = (description or "").strip()
    if not description:
        raise ApiError("INVALID_COURSE", "description is required", 400)
    return description


def _clean_duration(duration_hours: int) -> int:
    if duration_hours is None or duration_hours <= 0:
        raise ApiError("INVALID_COURSE", "duration_hours must be greater than zero", 400)
    return duration_hours


@router.get("")
def list_courses(
    current=Depends(require_scope("courses:read")),
    db: Session = Depends(get_db),
):
    return [course_out(c) for c in db.query(Course).order_by(Course.id).all()]


@router.get("/{course_id}")
def get_course(
    course_id: int,
    current=Depends(require_scope("courses:read")),
    db: Session = Depends(get_db),
):
    course = db.get(Course, course_id)
    if course is None:
        raise ApiError("COURSE_NOT_FOUND", f"no course with id {course_id}", 404)
    return course_out(course)


@router.post("", status_code=201)
def create_course(
    body: CourseCreate,
    current=Depends(require_scope("courses:write")),
    db: Session = Depends(get_db),
):
    course = Course(
        title=_clean_title(body.title),
        description=_clean_description(body.description),
        duration_hours=_clean_duration(body.duration_hours),
        status="ACTIVE",
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return course_out(course)


@router.put("/{course_id}")
def update_course(
    course_id: int,
    body: CourseUpdate,
    current=Depends(require_scope("courses:write")),
    db: Session = Depends(get_db),
):
    course = db.get(Course, course_id)
    if course is None:
        raise ApiError("COURSE_NOT_FOUND", f"no course with id {course_id}", 404)

    if body.title is not None:
        course.title = _clean_title(body.title)
    if body.description is not None:
        course.description = _clean_description(body.description)
    if body.duration_hours is not None:
        course.duration_hours = _clean_duration(body.duration_hours)
    if body.status is not None:
        status = body.status.strip().upper()
        if status not in ("ACTIVE", "INACTIVE"):
            raise ApiError("INVALID_COURSE", "status must be ACTIVE or INACTIVE", 400)
        course.status = status

    db.commit()
    db.refresh(course)
    return course_out(course)


@router.delete("/{course_id}", status_code=204)
def delete_course(
    course_id: int,
    current=Depends(require_scope("courses:write")),
    db: Session = Depends(get_db),
):
    course = db.get(Course, course_id)
    if course is None:
        raise ApiError("COURSE_NOT_FOUND", f"no course with id {course_id}", 404)
    db.delete(course)
    db.commit()
    return Response(status_code=204)

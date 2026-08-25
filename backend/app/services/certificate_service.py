from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from ..errors import ApiError
from ..models import Assessment, AssessmentAttempt, Assignment, Certificate, Course, Learner


def next_certificate_number(db: Session) -> str:
    year = datetime.now(timezone.utc).year
    count = (
        db.query(func.count(Certificate.id))
        .filter(Certificate.certificate_number.like(f"CERT-{year}-%"))
        .scalar()
    )
    return f"CERT-{year}-{count + 1:03d}"


def assert_eligible(db: Session, learner_id: int, course_id: int) -> None:
    assignment = (
        db.query(Assignment)
        .filter(Assignment.learner_id == learner_id, Assignment.course_id == course_id)
        .first()
    )
    if assignment is None or assignment.status != "COMPLETED":
        raise ApiError("NOT_ELIGIBLE", "course assignment is not completed", 409)

    latest_attempt = (
        db.query(AssessmentAttempt)
        .join(Assessment, AssessmentAttempt.assessment_id == Assessment.id)
        .filter(
            Assessment.course_id == course_id,
            AssessmentAttempt.learner_id == learner_id,
        )
        .order_by(AssessmentAttempt.id.desc())
        .first()
    )
    if latest_attempt is None or latest_attempt.result != "PASS":
        raise ApiError("NOT_ELIGIBLE", "course assessment has not been passed", 409)


def ensure_references_exist(db: Session, learner_id: int, course_id: int) -> None:
    if db.get(Learner, learner_id) is None:
        raise ApiError("LEARNER_NOT_FOUND", f"no learner with id {learner_id}", 404)
    if db.get(Course, course_id) is None:
        raise ApiError("COURSE_NOT_FOUND", f"no course with id {course_id}", 404)

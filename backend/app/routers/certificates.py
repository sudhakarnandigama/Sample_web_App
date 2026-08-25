from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..auth import CurrentUser, require_scope
from ..database import get_db
from ..errors import ApiError
from ..models import Certificate, Course, Learner
from ..schemas.certificate import CertificateGenerate
from ..services.certificate_service import (
    assert_eligible,
    ensure_references_exist,
    next_certificate_number,
)

router = APIRouter(prefix="/certificates", tags=["certificates"])


def certificate_out(cert: Certificate, learner_name: str = None, course_title: str = None) -> dict:
    data = {
        "id": cert.id,
        "learner_id": cert.learner_id,
        "course_id": cert.course_id,
        "certificate_number": cert.certificate_number,
        "issued_date": cert.issued_date,
        "status": cert.status,
    }
    if learner_name is not None:
        data["learner_name"] = learner_name
    if course_title is not None:
        data["course_title"] = course_title
    return data


@router.get("")
def list_certificates(
    current: CurrentUser = Depends(require_scope("certificates:read")),
    db: Session = Depends(get_db),
):
    query = (
        db.query(Certificate, Learner.name, Course.title)
        .join(Learner, Certificate.learner_id == Learner.id)
        .join(Course, Certificate.course_id == Course.id)
    )
    if current.role == "LEARNER":
        query = query.filter(Certificate.learner_id == current.learner_id)
    rows = query.order_by(Certificate.id).all()
    return [certificate_out(c, learner_name=ln, course_title=ct) for c, ln, ct in rows]


@router.get("/{certificate_id}")
def get_certificate(
    certificate_id: int,
    current: CurrentUser = Depends(require_scope("certificates:read")),
    db: Session = Depends(get_db),
):
    cert = db.get(Certificate, certificate_id)
    if cert is None:
        raise ApiError("CERTIFICATE_NOT_FOUND", f"no certificate with id {certificate_id}", 404)
    if current.role == "LEARNER" and cert.learner_id != current.learner_id:
        raise ApiError("CERTIFICATE_NOT_FOUND", f"no certificate with id {certificate_id}", 404)

    learner = db.get(Learner, cert.learner_id)
    course = db.get(Course, cert.course_id)
    return certificate_out(cert, learner_name=learner.name, course_title=course.title)


@router.post("", status_code=201)
def generate_certificate(
    body: CertificateGenerate,
    current: CurrentUser = Depends(require_scope("certificates:write")),
    db: Session = Depends(get_db),
):
    if current.role == "ADMIN":
        learner_id = body.learner_id
        if learner_id is None:
            raise ApiError("INVALID_CERTIFICATE", "learner_id is required for admin", 400)
    else:
        learner_id = current.learner_id
        if learner_id is None:
            raise ApiError("INSUFFICIENT_SCOPE", "learner account is not linked to a learner record", 403)

    ensure_references_exist(db, learner_id, body.course_id)

    existing = (
        db.query(Certificate)
        .filter(Certificate.learner_id == learner_id, Certificate.course_id == body.course_id)
        .first()
    )
    if existing is not None:
        raise ApiError("CERTIFICATE_EXISTS", "certificate already issued for this course", 409)

    assert_eligible(db, learner_id, body.course_id)

    cert = Certificate(
        learner_id=learner_id,
        course_id=body.course_id,
        certificate_number=next_certificate_number(db),
        status="CERTIFIED",
    )
    db.add(cert)
    db.commit()
    db.refresh(cert)
    learner = db.get(Learner, cert.learner_id)
    course = db.get(Course, cert.course_id)
    return certificate_out(cert, learner_name=learner.name, course_title=course.title)

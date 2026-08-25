from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..auth import CurrentUser, require_scope
from ..database import get_db
from ..errors import ApiError
from ..models import Assessment, AssessmentAttempt, Learner, Question
from ..schemas.assessment import SubmitAnswers
from ..services.assessment_service import score_submission

router = APIRouter(prefix="/assessments", tags=["assessments"])


@router.get("/attempts")
def list_attempts(
    current: CurrentUser = Depends(require_scope("reports:read")),
    db: Session = Depends(get_db),
):
    rows = (
        db.query(AssessmentAttempt, Assessment.course_id, Learner.name)
        .join(Assessment, AssessmentAttempt.assessment_id == Assessment.id)
        .join(Learner, AssessmentAttempt.learner_id == Learner.id)
        .order_by(AssessmentAttempt.id)
        .all()
    )
    return [
        {
            "id": attempt.id,
            "assessment_id": attempt.assessment_id,
            "learner_id": attempt.learner_id,
            "course_id": course_id,
            "score": attempt.score,
            "result": attempt.result,
            "attempted_at": attempt.attempted_at,
            "learner_name": learner_name,
        }
        for attempt, course_id, learner_name in rows
    ]


@router.get("/{course_id}")
def get_assessment(
    course_id: int,
    current=Depends(require_scope("assessments:read")),
    db: Session = Depends(get_db),
):
    assessment = db.query(Assessment).filter(Assessment.course_id == course_id).first()
    if assessment is None:
        raise ApiError("ASSESSMENT_NOT_FOUND", f"no assessment for course {course_id}", 404)

    questions = (
        db.query(Question).filter(Question.assessment_id == assessment.id).order_by(Question.id).all()
    )
    return {
        "id": assessment.id,
        "course_id": assessment.course_id,
        "title": assessment.title,
        "passing_score": assessment.passing_score,
        "questions": [
            {
                "id": q.id,
                "question_text": q.question_text,
                "option_a": q.option_a,
                "option_b": q.option_b,
                "option_c": q.option_c,
                "option_d": q.option_d,
            }
            for q in questions
        ],
    }


@router.post("/{assessment_id}/submit")
def submit_assessment(
    assessment_id: int,
    body: SubmitAnswers,
    current: CurrentUser = Depends(require_scope("assessments:submit")),
    db: Session = Depends(get_db),
):
    assessment = db.get(Assessment, assessment_id)
    if assessment is None:
        raise ApiError("ASSESSMENT_NOT_FOUND", f"no assessment with id {assessment_id}", 404)

    if body.answers is None:
        raise ApiError("INVALID_SUBMISSION", "answers are required", 400)
    if current.learner_id is None:
        raise ApiError("INSUFFICIENT_SCOPE", "learner account is not linked to a learner record", 403)

    score, result = score_submission(db, assessment, body.answers)

    attempt = AssessmentAttempt(
        assessment_id=assessment_id,
        learner_id=current.learner_id,
        score=score,
        result=result,
    )
    db.add(attempt)
    db.commit()
    return {"score": score, "result": result}

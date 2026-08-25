from sqlalchemy.orm import Session

from ..errors import ApiError
from ..models import Assessment, Question


def score_submission(db: Session, assessment: Assessment, answers: dict) -> tuple[int, str]:
    questions = db.query(Question).filter(Question.assessment_id == assessment.id).all()
    valid_ids = {str(q.id) for q in questions}

    for key in answers:
        if key not in valid_ids:
            raise ApiError("INVALID_SUBMISSION", f"unknown question id {key}", 400)

    if not questions:
        return 0, "FAIL"

    correct = 0
    for q in questions:
        option = answers.get(str(q.id))
        if option not in ("A", "B", "C", "D"):
            raise ApiError("INVALID_SUBMISSION", "answers must be one of A, B, C, D", 400)
        if option == q.correct_option:
            correct += 1

    score = round(correct / len(questions) * 100)
    result = "PASS" if score >= assessment.passing_score else "FAIL"
    return score, result

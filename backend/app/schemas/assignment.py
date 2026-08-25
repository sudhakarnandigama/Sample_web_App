from typing import Optional

from pydantic import BaseModel


class AssignmentCreate(BaseModel):
    learner_id: int
    course_id: int


class ProgressUpdate(BaseModel):
    progress: int
    status: Optional[str] = None

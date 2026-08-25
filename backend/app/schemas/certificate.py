from typing import Optional

from pydantic import BaseModel


class CertificateGenerate(BaseModel):
    learner_id: Optional[int] = None
    course_id: int

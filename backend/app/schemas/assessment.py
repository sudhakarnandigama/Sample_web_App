from typing import Dict, Optional

from pydantic import BaseModel


class SubmitAnswers(BaseModel):
    answers: Optional[Dict[str, str]] = None

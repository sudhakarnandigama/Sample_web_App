from typing import Optional

from pydantic import BaseModel


class LearnerCreate(BaseModel):
    name: str
    email: str
    department: str


class LearnerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None
    status: Optional[str] = None
